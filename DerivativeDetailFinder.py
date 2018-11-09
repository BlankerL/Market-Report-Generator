from WindPy import *
import datetime


class Session:
    def __init__(self, stock_id, date_input):
        self.stock_id = stock_id
        self.date_input = date_input  # Need to be a str

    def data_manage(self):
        # Because the data today usually be unreachable in WSS,
        # if the date_input is date today, the amt is reported by WSQ,
        # otherwise, it will be reported by WSS
        date_today = datetime.date.today().strftime('%Y%m%d')
        is_get_dynamic = 0
        if self.date_input == date_today:
            # TODO: Check the use of wss/wsq in SDF
            get_static = w.wss(self.stock_id,
                               "SEC_NAME,WINDCODE",
                               "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
            get_dynamic = w.wsq(self.stock_id,
                                "RT_CHG,RT_PCT_CHG,RT_LAST,RT_OI,RT_OI_CHG,RT_SPREAD,RT_VOL")
            is_get_dynamic = 1
        else:
            # If the date is one day later,
            # it will access the WSS database because the WSQ real time data is not the data required.
            get_static = w.wss(self.stock_id,
                               "SEC_NAME,WINDCODE,CHG,PCT_CHG,CLOSE,OI,OI_CHG,VOLUME,IF_BASIS",
                               "tradeDate=%s;priceAdj=U;cycle=D" % self.date_input)
        data_dict = {}
        # Use the name dict to make the names all the same
        name_dict = {
            'SEC_NAME': 'SEC_NAME',
            'WINDCODE': 'WINDCODE',
            'RT_CHG': 'CHG',
            'CHG': 'CHG',
            'RT_PCT_CHG': 'PCT_CHG',
            'PCT_CHG': 'PCT_CHG',
            'RT_LAST': 'CLOSE',
            'CLOSE': 'CLOSE',
            'RT_AMT': 'AMT',
            'AMT': 'AMT',
            'RT_OI': 'OPEN_INTEREST',
            'OI': 'OPEN_INTEREST',
            'RT_OI_CHG': 'OPEN_INTEREST_CHG',
            'OI_CHG': 'OPEN_INTEREST_CHG',
            'RT_SPREAD': 'SPREAD',
            'IF_BASIS': 'SPREAD',
            'RT_VOL': 'VOLUME',
            'VOLUME': 'VOLUME'
        }
        for i in range(len(get_static.Codes)):
            codes = get_static.Codes[i]
            data_dict[codes] = {}
            for j in range(len(get_static.Fields)):
                data_name = name_dict[get_static.Fields[j]]
                data_dict[codes][data_name] = get_static.Data[j][i]
            if is_get_dynamic == 1:
                for j in range(len(get_dynamic.Fields)):
                    data_name = name_dict[get_dynamic.Fields[j]]
                    data_dict[codes][data_name] = get_dynamic.Data[j][i]
            else:
                pass
        return data_dict

    def data_printer(self):
        data_dict = self.data_manage()
        return data_dict[self.stock_id]['SEC_NAME'], round(data_dict[self.stock_id]['PCT_CHG'], 2), \
            round(data_dict[self.stock_id]['CHG'], 2), round(data_dict[self.stock_id]['CLOSE'], 1), \
            int(data_dict[self.stock_id]['OPEN_INTEREST']), int(data_dict[self.stock_id]['OPEN_INTEREST_CHG']), \
            int(data_dict[self.stock_id]['VOLUME']), round(data_dict[self.stock_id]['SPREAD'], 2)
