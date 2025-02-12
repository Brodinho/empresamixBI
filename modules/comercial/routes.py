from flask import render_template
import logging
from .components import TerritoryMap, RegionRanking
from .services.api_service import ComercialAPIService

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/comercial/analise-territorial')
def analise_territorial():
    logger.info("Iniciando carregamento da análise territorial")
    
    try:
        # Obtém os dados
        df = ComercialAPIService.get_vendas_mapa()
        logger.info(f"Dados carregados: {len(df)} registros")
        
        # Cria o mapa
        territory_map = TerritoryMap.create_scatter_mapbox(df)
        logger.info("Mapa criado com sucesso")
        
        # Cria o ranking
        logger.info("Iniciando criação do ranking")
        region_ranking = RegionRanking.create_ranking_chart(df)
        logger.info("Ranking criado com sucesso")
        
        # Debug dos dados do ranking
        top_5 = df.nlargest(5, 'faturamento')
        logger.info(f"Top 5 regiões: {top_5[['location_name', 'faturamento']].to_dict('records')}")
        
        return render_template(
            'comercial/analise_territorial.html',
            territory_map=territory_map.to_html(
                full_html=False,
                include_plotlyjs=True
            ),
            region_ranking=region_ranking.to_html(
                full_html=False,
                include_plotlyjs=False
            )
        )
    except Exception as e:
        logger.error(f"Erro na rota analise_territorial: {str(e)}", exc_info=True)
        return f"Erro ao carregar os dados: {str(e)}" 