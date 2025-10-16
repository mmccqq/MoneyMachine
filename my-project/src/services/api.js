import axios from 'axios'

// Base axios instance
const http = axios.create({
  baseURL: '', // set to your API base if you have one
  timeout: 10000
})

/*
Expected API shapes:
- GET /api/stocks?q=...   => [{ code, name, price, change }, ...]
- GET /api/summary/:code  => { open, prevClose, high, low }
- GET /api/kline/:code    => { categories: ['第1日','第2日',...], values: [[open,close,low,high], ...] }
*/

const mockStocks = [
  { code: '600519', name: '贵州茅台', price: 1765.00, change: 0.0245 },
  { code: '300750', name: '宁德时代', price: 215.80, change: -0.0087 },
  { code: '601318', name: '中国平安', price: 45.23, change: 0.0072 },
  { code: '600036', name: '招商银行', price: 32.56, change: 0.0125 },
  { code: '000858', name: '五粮液', price: 167.32, change: 0.0182 },
  { code: '601888', name: '中国中免', price: 108.45, change: -0.0034 }
]

const makeMockKline = () => {
  const categories = []
  const values = []
  let base = 1650
  for (let i = 1; i <= 100; i++) {
    categories.push(`第${i}日`)
    const open = +(base + (Math.random() - 0.5) * 30).toFixed(2)
    const close = +(open + (Math.random() - 0.5) * 20).toFixed(2)
    const low = Math.min(open, close) - +(Math.random() * 5).toFixed(2)
    const high = Math.max(open, close) + +(Math.random() * 5).toFixed(2)
    values.push([open, close, low, high])
    base += (Math.random() - 0.5) * 10
  }
  return { categories, values }
}

export default {
  async getStocks({ q } = {}) {
    // Replace with real API call:
    // const resp = await http.get('/api/stocks', { params: { q } })
    // return resp.data
    // MOCK:
    if (!q) return mockStocks
    const lower = q.toLowerCase()
    return mockStocks.filter(s => s.name.includes(q) || s.code.includes(q))
  },

  // async getSummary(code) {
  //   // Replace with: return (await http.get(`/api/summary/${code}`)).data
  //   // MOCK:
  //   return {
  //     open: +(1600 + Math.random() * 150).toFixed(2),
  //     prevClose: +(1600 + Math.random() * 150).toFixed(2),
  //     high: +(1700 + Math.random() * 120).toFixed(2),
  //     low: +(1500 + Math.random() * 120).toFixed(2)
  //   }
  // },

  async getKline(code) {
    // Replace with: return (await http.get(`/api/kline/${code}`)).data
    // MOCK:
    return makeMockKline()
  },

  async getStockData(stock_id) {
    const where_column = "date <= ";
    const where_condition = new Date().toISOString().split('T')[0];
    const limit = 250;
    const order = "date DESC";
    const response = await fetch(
      `http://127.0.0.1:5000/api/stock_id_data?stock_id=${stock_id}&order_by=${order}&limit=${limit}&where_column=${where_column}&where_condition=${where_condition}`
    );
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const categories = []
    const values = []
    return await response.json();
  },

  async update() {
    const response = await fetch(`http://127.0.0.1:5000/api/update`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  },

  async getAllStocks({ q } = {}) {
    const response = await fetch(`http://127.0.0.1:5000/api/id_lst`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  },

  async getSuggestedStocks({ q } = {}) {
    const response = await fetch(`http://127.0.0.1:5000/api/suggested_id_lst`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  },

  async getSummary(stock_id) {
    const limit = 1;
    const order = "date DESC";
    const response = await fetch(
      `http://127.0.0.1:5000/api/stock_id_data?stock_id=${stock_id}&order_by=${order}&limit=${limit}`
    );
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json()
    const [open, close, low, high] = data.values[0]
  return { high, low, close, open };
  }

}