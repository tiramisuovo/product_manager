import '../styles/output.css';
import { useState } from 'react';
import { searchProducts } from '../utils/api';
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import ProductList from "./ProductList";
import ProductDetails from "./ProductDetails";
import Dropdown from "./Dropdown";


function App() {
  const [text, setText] = useState('');
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('name');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const navigate = useNavigate();

  async function handleSearch() {
    const results = await searchProducts({ [selectedCategory]: text });
    setProducts(results);
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col relative">
      {/* Navbar */}
      <nav className="bg-slate-600 text-white px-8 py-4 flex gap-8 shadow-md">
        <Link to="/" className="hover:underline font-medium">
          🔍 Search
        </Link>
        <Link to="/ProductDetails" className="hover:underline font-medium">
          📦 Product Details
        </Link>
      </nav>

      {/* Content */}
      <main className="flex-1 p-8 max-w-5xl mx-auto w-full">
        <Routes>
          {/* Search page */}
          <Route
            path="/"
            element={
              <div className="space-y-8">
                <h2 className="text-3xl font-bold text-slate-700">
                  Product Search
                </h2>

                <div className="flex gap-4 items-center">
                  <Dropdown
                    selectedCategory={selectedCategory}
                    setSelectedCategory={setSelectedCategory}
                  />

                  <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Search..."
                    className="flex-1 px-4 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
                  />

                  <button
                    onClick={handleSearch}
                    className="px-6 py-2 bg-slate-500 hover:bg-slate-600 text-white rounded-md font-medium transition"
                  >
                    Confirm
                  </button>
                </div>

                <div>
                  <h4 className="text-xl font-semibold mb-3">Product List</h4>
                  <ProductList
                    products={products}
                    onSelect={(product) => {
                      setSelectedProduct(product);
                      navigate('/ProductDetails');
                    }}
                  />
                </div>
              </div>
            }
          />

          {/* Product details page */}
          <Route
            path="/ProductDetails"
            element={
              selectedProduct ? (
                <ProductDetails
                  product={selectedProduct}
                  onClose={() => setSelectedProduct(null)}
                />
              ) : (
                <p className="text-slate-500 italic">No product selected</p>
              )
            }
          />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="absolute bottom-2 right-2 px-3 py-2 rounded-md text-xs italic font-serif text-slate-500">
        Powered by @tiramisuovo
      </footer>
    </div>
  );
}

export default App;

