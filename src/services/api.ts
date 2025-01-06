export const getFaturamentoTerritorial = async () => {
  try {
    const response = await api.get('/', {
      params: {
        CLIENTE: import.meta.env.VITE_API_CLIENTE,
        ID: import.meta.env.VITE_API_ID,
        VIEW: import.meta.env.VITE_API_VIEW
      }
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar dados territoriais:', error);
    throw new Error('Erro ao buscar dados territoriais');
  }
}; 