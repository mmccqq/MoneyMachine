<template>
  <div class="app">
    <!-- Add notification component -->
    <transition name="fade">
      <div v-if="notification.show" class="notification">
        {{ notification.message }}
      </div>
    </transition>


    <aside class="sidebar">
      <!-- <div class="search">
        <input v-model="query" placeholder="Search stock id or name..." @keyup.enter="search" />
        <button class="btn" @click="search">Search</button>
      </div> -->

      <div class="stock-list">
        <div
          v-for="s in stocks"
          :key="s.code"
          class="stock-item"
          :class="{selected: selected && selected.code === s.code}"
          @click="selectStock(s)"
        >
          <div class="stock-left">
            <div class="price">{{ s.name }}</div>
            <div class="small">{{ s.code }}</div>
          </div>
          <div style="text-align:right">
            <div :class="s.change >= 0 ? 'positive price' : 'negative price'">
              {{ formatNumber(s.price) }}
            </div>
            <div class="small" :class="s.change >=0 ? 'positive' : 'negative'">
              {{ s.change >= 0 ? '+' : ''}}{{ (s.change * 100).toFixed(2) }}%
            </div>
          </div>
        </div>
      </div>
    </aside>

    <main class="main">
      <div class="header">
        <div class="summary" v-if="selected">
          <div class="title">{{ selected.name }} <small class="small"> {{ selected.code }}</small></div>
          <div class="price">{{ formatNumber(selected.price) }} <span :class="selected.change>=0 ? 'positive' : 'negative'"> {{ selected.change >=0 ? '+' : ''}}{{ (selected.change*100).toFixed(2) }}%</span></div>
          <div class="meta">
            <div>open <b>{{ formatNumber(summary.open) }}</b></div>
            <div>close <b>{{ formatNumber(summary.prevClose) }}</b></div>
            <div>high <b>{{ formatNumber(summary.high) }}</b></div>
            <div>low <b>{{ formatNumber(summary.low) }}</b></div>
          </div>
        </div>

        <div class="controls">
          <button class="btn" @click="updateList">update list</button>
          <button class="btn" @click="fetchChart">update graph</button>
          <div class="btn">indicators: <strong style="margin-left:8px">MA10, 20</strong></div>
          <div class="btn">frequency: <strong style="margin-left:8px">day Kl</strong></div>
        </div>
      </div>

      <div class="chart-card" v-if="selected">
        <div class="kline-legend">day Kline Graph - {{ selected.name }} ({{ selected.code }})</div>
        <div class="chart-wrap" ref="chartEl"></div>
        <div style="margin-top:12px;display:flex;justify-content:space-between;align-items:center">
          <div class="footer-legend">
            <span class="ma-badge">MA (10)</span>
            <span class="ma-badge">MA (20)</span>
            <span class="small">data source: API</span>
          </div>
          <div class="small">display latest {{ kData.length }} days</div>
        </div>
      </div>

      <div v-else class="chart-card">
        <div style="padding:40px;color:var(--muted)"> select stock at left for details</div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import api from './services/api'
import * as echarts from 'echarts'

export default {
  setup() {
    const query = ref('')
    const stocks = ref([])
    const selected = ref(null)
    const summary = ref({ open: 0, prevClose: 0, high: 0, low: 0 })
    const chartEl = ref(null)
    const chart = ref(null)
    const kData = ref([])
    const notification = ref({ show: false, message: '' })


    const formatNumber = (v) => (typeof v === 'number' ? v.toFixed(2) : v)

    async function fetchStocks() {
      try {
        // const res = await api.getStocks({ q: query.value })
        const res = await api.getAllStocks({ q: query.value })
        // expected res = [{code, name, price, change}, ...]
        stocks.value = res
        if (!selected.value && stocks.value.length) selectStock(stocks.value[0])
      } catch (err) {
        console.error(err)
      }
    }

    async function updateList() {
      try {
        const res = await api.update()
        showNotification(`Stock list updated: ${res.updated} items.`)
        fetchStocks()
      } catch (err) {
        console.error(err)
        showNotification('Failed to update stock list.')
      }
    }

    // click the stock in the list
    async function selectStock(s) {
      selected.value = s
      await fetchSummary()
      fetchChart()
    }

    async function fetchSummary() {
      if (!selected.value) return
      try {
        const res = await api.getSummary(selected.value.code)
        // expected res = {open, prevClose, high, low}
        summary.value = res
      } catch (err) {
        console.error(err)
      }
    }

    async function fetchChart() {
      if (!selected.value) return
      try {
        // const res = await api.getKline(selected.value.code)
        const res = await api.getStockData(selected.value.code)
        // expected res = { categories: [...dates], values: [[open, close, low, high], ...] }
        kData.value = res
        renderChart()
      } catch (err) {
        console.error(err)
      }
    }

    function showNotification(message) {
      notification.value = { show: true, message }
      setTimeout(() => {
        notification.value.show = false
      }, 3000)
    }

    function renderChart() {
      if (!chartEl.value) return
      if (!chart.value) {
        chart.value = echarts.init(chartEl.value)
        window.addEventListener('resize', () => chart.value && chart.value.resize())
        chart.value.on('updateAxisPointer', function(event) {
          const xAxisInfo = event.axesInfo[0]
          if (xAxisInfo) {
            const dataIndex = xAxisInfo.value
            if (dataIndex >= 0 && dataIndex < kData.value.values.length) {
              const [open, close, low, high] = kData.value.values[dataIndex]
              // Update summary with hovered values
              summary.value = {
                open: open,
                prevClose: summary.value.prevClose, // Keep original
                high: high,
                low: low
              }
            }
          }
        })
      }
      const option = buildKlineOption(kData.value)
      chart.value.setOption(option)
    }

    function buildKlineOption(k) {
      // k: { categories:[], values:[] }
      const categories = k.categories || []
      const values = k.values || []

      // compute MA (simple)
      const calcMA = (dayCount) => {
        const result = []
        for (let i = 0; i < values.length; i++) {
          if (i < dayCount - 1) {
            result.push('-')
            continue
          }
          let sum = 0
          for (let j = 0; j < dayCount; j++) {
            sum += values[i - j][1] // close price index 1
          }
          result.push((sum / dayCount).toFixed(2))
        }
        return result
      }

      return {
        backgroundColor: 'transparent',
        // tooltip: {
        //   trigger: 'axis',
        //   axisPointer: { type: 'cross' },
        //   backgroundColor: 'rgba(50, 50, 50, 0.8)',
        //   borderWidth: 0,
        //   textStyle: { color: '#fff' },
        //   formatter: function (params) {
        //     console.log('Tooltip params:', params)
        //     const k = params.find(p => p.seriesName === 'K')
        //     if (!k) return ''
        //     const [open, close, low, high] = k.data
        //     const date = k.axisValue
        //     return `
        //       <div style="padding:6px 10px;line-height:1.6">
        //         <strong>${date}</strong><br/>
        //         Open: ${open.toFixed(2)}<br/>
        //         Close: ${close.toFixed(2)}<br/>
        //         High: ${high.toFixed(2)}<br/>
        //         Low: ${low.toFixed(2)}
        //       </div>
        //     `
        //   }
        // },


        // tooltip: {
        //   show: true,  // Explicitly enable
        //   trigger: 'axis',
        //   axisPointer: { 
        //     type: 'cross',
        //     animation: false,
        //     label: {
        //       backgroundColor: '#ffd208'
        //     }
        //   }
        // },

        tooltip: {
          show: true,
          trigger: 'axis',
          axisPointer: { 
            type: 'cross',
            animation: false,
            label: {
              backgroundColor: '#ffd208'
            }
          },
          // Add custom formatter to capture hover data
          formatter: function(params) {
            // This will be called on hover
            return params[0].name; // Return something for the tooltip display
          }
        },

        // tooltip: {
        //   trigger: 'axis',
        //   axisPointer: { type: 'cross' }
        // },
        grid: { left: '8%', right: '8%', bottom: '10%' },
        xAxis: {
          type: 'category',
          data: categories,
          axisLine: { lineStyle: { color: '#2b3b43' } },
          axisLabel: { color: '#9aa6b2' }
        },
        yAxis: {
          scale: true,
          axisLine: { lineStyle: { color: '#2b3b43' } },
          axisLabel: { color: '#9aa6b2' }
        },
        dataZoom: [
          {
            type: 'inside',
            zoomOnMouseWheel: false,  // disable zooming
            moveOnMouseMove: true,    // allow moving
            moveOnMouseWheel: true,   // allow horizontal move using wheel
            preventDefaultMouseMove: false
          },
          {
            type: 'slider',
            show: true,
            zoomLock: true,           // lock zoom level
            handleSize: 0,            // hide handles if you want
            height: 10,
            bottom: 0
          }
        ],
        series: [
          {
            name: 'K',
            type: 'candlestick',
            data: values,
            itemStyle: {
              color: '#2bd37b',
              color0: '#ff6b6b',
              borderColor: '#2bd37b',
              borderColor0: '#ff6b6b'
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: calcMA(10),
            smooth: true,
            lineStyle: { width: 2 },
            showSymbol: false
          },
          {
            name: 'MA20',
            type: 'line',
            data: calcMA(20),
            smooth: true,
            lineStyle: { width: 2 },
            showSymbol: false
          }
        ]
      }
    }

    function search() {
      fetchStocks()
    }

    onMounted(() => {
      fetchStocks()
    })

    // expose to template
    return {
      query,
      stocks,
      selected,
      summary,
      chartEl,
      kData,
      fetchStocks,
      notification,
      updateList,
      fetchChart,
      selectStock,
      formatNumber,
      search
    }
  }
}
</script>

<style scoped>
/* local component tweaks if needed */
.chart-wrap { width:100%; height:100%;
pointer-events: auto !important; }
.chart-card {
  pointer-events: auto !important;
}

.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #2bd37b;
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  z-index: 1000;
  font-weight: 500;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>