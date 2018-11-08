from WindPy import *
import Services

class StockDetailFinder:
    def __init__(self, derivative_id, date_input):
        self.stock_id = stock_id
        self.date_input = date_input  # Need to be a str

    def data_manage(self):
        get_name = w.wss(self.stock_id,
                         "SEC_NAME,WINDCODE",
                         "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        get_data = w.wsq(self.stock_id,
                         "RT_CHG,RT_PCT_CHG,rt_last,rt_amt",
                         "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        data_dict = {}
        for i in range(len(get_name.Codes)):
            codes = get_name.Codes[i]
            data_dict[codes] = {}
            for j in range(len(get_name.Fields)):
                data_name = get_name.Fields[j]
                data_dict[codes][data_name] = get_name.Data[j][i]
            for j in range(len(get_data.Fields)):
                data_name = get_data.Fields[j]
                data_dict[codes][data_name] = get_data.Data[j][i]
        return data_dict

    def data_printer(self):
        data_dict = self.data_manage()
        return data_dict[self.stock_id]['SEC_NAME'], round(data_dict[self.stock_id]['RT_PCT_CHG']*100, 2), \
            round(data_dict[self.stock_id]['RT_CHG'], 2), round(data_dict[self.stock_id]['RT_LAST'], 2), \
            data_dict[self.stock_id]['RT_AMT']