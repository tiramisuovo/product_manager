import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchImages } from "../utils/api";

function ProductDetails({ product, onClose }) {
  const navigate = useNavigate();
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null); // for modal

  const tagSummary = Array.isArray(product?.tags)
    ? product.tags
        .map((tag) => (typeof tag === 'string' ? tag : tag?.tag_name))
        .filter(Boolean)
        .join(', ')
    : product?.tag ?? '';

  useEffect(() => {
    if (product?.id) {
      fetchImages(product.id).then(setImages);
    }
  }, [product]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 p-8">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Back button */}
        <button
          onClick={() => {
            onClose();
            navigate("/");
          }}
          className="px-4 py-2 bg-slate-500 hover:bg-slate-600 text-white rounded-md transition font-medium"
        >
          ← Back
        </button>

        {/* Product header */}
        <h2 className="text-2xl font-bold text-slate-700">
          {product?.name || "Unnamed Product"}
        </h2>

        {/* Product info */}
        <div className="space-y-2 text-slate-700">
          <p><span className="font-semibold">Ref Number:</span> {product?.ref_num}</p>
          <p><span className="font-semibold">Tags:</span> {product?.tags}</p>
          <p><span className="font-semibold">Barcode:</span> {product?.barcode}</p>
          <p><span className="font-semibold">Pcs/inner box:</span> {product?.pcs_innerbox}</p>
          <p><span className="font-semibold">Pcs/ctn:</span> {product?.pcs_ctn}</p>
          <p><span className="font-semibold">Weight:</span> {product?.weight}</p>
          <p><span className="font-semibold">Packing:</span> {product?.packing}</p>
          <p><span className="font-semibold">Price (USD):</span> ${product?.price_usd}</p>
        </div>

        {/* Images */}
        <div>
          <h3 className="text-lg font-semibold mb-2">Images</h3>
          {images.length > 0 ? (
            <div className="flex flex-wrap gap-4">
              {images.map((url, idx) => (
                <img
                  key={idx}
                  src={url}
                  alt={product?.name}
                  className="w-48 h-48 object-cover rounded-md border border-slate-200 shadow-sm cursor-pointer hover:scale-105 transition"
                  onClick={() => setSelectedImage(url)}
                />
              ))}
            </div>
          ) : (
            <p className="text-slate-500 italic">No images found</p>
          )}
        </div>
      </div>

      {/* Modal for enlarged image */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50"
          onClick={() => setSelectedImage(null)}
        >
          <img
            src={selectedImage}
            alt="Enlarged"
            className="max-w-3xl max-h-[90vh] rounded-lg shadow-lg"
          />
        </div>
      )}


    </div>

    
  );
}

export default ProductDetails;
