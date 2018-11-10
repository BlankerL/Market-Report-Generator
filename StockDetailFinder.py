from WindPy import *
import datetime


class StockDetailFinder:
    def __init__(self, stock_id, date_input):
        self.stock_id = stock_id
        self.date_input = date_input  # Need to be a str

    def data_manage(self):
        # Because the data today usually be unreachable in WSS,
        # if the date_input is date today, the amt is reported by WSQ,
        # otherwise, it will be reported by WSS
        date_today = datetime.date.today().strftime('%Y%m%d')
        if self.date_input == date_today:
            get_name = w.wss(self.stock_id,
                             "SEC_NAME,WINDCODE",
                             "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
            get_data = w.wsq(self.stock_id,
                             "RT_CHG,RT_PCT_CHG,RT_LAST,RT_AMT",
                             "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        else:
            get_name = w.wss(self.stock_id,
                             "SEC_NAME,WINDCODE,AMT",
                             "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
            get_data = w.wsq(self.stock_id,
                             "RT_CHG,RT_PCT_CHG,RT_LAST",
                             "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        data_dict = {}
        # Use the name dict to make the names all the same
        name_dict = {
            'SEC_NAME': 'SEC_NAME',
            'WINDCODE': 'WINDCODE',
            'RT_CHG': 'CHG',
            'RT_PCT_CHG': 'PCT_CHG',
            'RT_LAST': 'LAST',
            'RT_AMT': 'AMT',
            'AMT': 'AMT'
        }
        for i in range(len(get_name.Codes)):
            codes = get_name.Codes[i]
            data_dict[codes] = {}
            for j in range(len(get_name.Fields)):
                data_name = name_dict[get_name.Fields[j]]
                data_dict[codes][data_name] = get_name.Data[j][i]
            for j in range(len(get_data.Fields)):
                data_name = name_dict[get_data.Fields[j]]
                data_dict[codes][data_name] = get_data.Data[j][i]
        return data_dict

    def data_printer(self):
        data_dict = self.data_manage()
        # For the foreign stock index, the amt is not available in Wind
        return data_dict[self.stock_id]['SEC_NAME'], round(data_dict[self.stock_id]['PCT_CHG']*100, 2), \
            round(data_dict[self.stock_id]['CHG'], 2), round(data_dict[self.stock_id]['LAST'], 2), \
            data_dict[self.stock_id]['AMT']
