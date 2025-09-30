function Dropdown({ selectedCategory, setSelectedCategory }) {
  const options = ["ref_num", "name", "tag", "customer", "barcode"];

  return (
    <div>
      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
        className="border border-slate-300 rounded-md px-3 py-2"
      >
        {options.map((opt, i) => (
          <option key={i} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}

export default Dropdown;