from JCOTSERVICE import MovimentoResumidoService  , RelPosicaoFundoCotistaService



class ArquivoRetornoManager(): 


    OT_ORDENS_RETORNO = {

        "Numero Operacao": [] , 
        "Investidor": []	 , 
        "Conta Corrente":  [],
        "Papel Cota": [], 
        'Ponto Venda': [] , 
        "Tipo Operacao": [], 
        "Data Operacao": [], 
        "Data Conversao": [], 
        "Data Liquidacao": 	[] , 
        "Data do Fundo na Movimentacao"	 : [] , 
        "Valor"	: [] ,  
        "Status": [], 
        "Status Conversao": [], 
        "CNPJ do fundo": [],
    }

    OT_POSICAO =  {
        "Mnêmonico Investidor": [] ,	
        "Investidor": [] ,	
        "CPF/CNPJ Investidor"	: [] ,
        "Data Referência": [] ,	
        "Papel Cota":  [],	
        "CNPJ Fundo": [] ,
        "Quantidade Total": [] ,	
        "Valor Bruto": [] , 
        "Cota": [],

    }



