const apiURL = process.env.REACT_APP_BASE_URL;

export async function searchProducts(filters = {}) {
  try {
    const params = new URLSearchParams(
      Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== undefined && v !== null)
      )
    ).toString();

    const response = await fetch(`${apiURL}/products/search?${params}`);
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
    
    const data = await response.json();
    console.log("Fetched products:", data);
    return data;

  } catch (err) {
    console.error("Error fetching products:", err);
    return [];
  }
}

export async function fetchImages(product_id){
  try {
    const response = await fetch(`${apiURL}/products/${product_id}/images/list`);
    if (!response.ok) throw new Error('HTTP error' + response.status);
    
    const data = await response.json();
    console.log("Fetched images:", data);
    return data;
  } catch (err) {
    console.error("Error fetching images:", err);
    return [];
  }
}