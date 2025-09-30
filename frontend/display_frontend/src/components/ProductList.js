function ProductList({ products, onSelect }) {
  return (
    <ul className="border border-slate-200 rounded-lg divide-y divide-slate-200">
      {products.map((p) => (
        <li
          key={p.id}
          onClick={() => onSelect(p)}
          className="px-4 py-3 cursor-pointer hover:bg-slate-200 hover:text-sky-700 transition-colors"
        >
          <span className="font-medium text-slate-800">{p.name}</span>
          <span className="text-slate-500"> (Ref: {p.ref_num})</span>
        </li>
      ))}
    </ul>
  );
}

export default ProductList;