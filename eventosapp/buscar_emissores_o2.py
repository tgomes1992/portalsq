

def get_emissor(ativos_o2 , codigo):

    try:
        return ativos_o2[ativos_o2['codigo'] == codigo ].to_dict("records")[0]
    except Exception as e:
        return {
            "nomeEmissor": 'na' , 
            "dataFimRelacionamento": "na"
        }
