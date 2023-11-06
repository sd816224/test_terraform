
from datetime import datetime as dt


def format_dim_date(table):

    '''
    argument:sales_order_content
        type:dict  
            key: table name
            value: updated content (list of dictionary)

    return:
        type: list of list
    '''
    
    content=table['sales_order']
    print(content)
    result=[]
    # for row in content:
    #     datetime=dt.strptime(row['agreed_delivery_date'],'%Y-%m-%d')

    #     datetime2=dt.strptime(row['created_at'][:10],'%Y-%m-%d')
    #     print(datetime,datetime2)
    


    list=[dt.]