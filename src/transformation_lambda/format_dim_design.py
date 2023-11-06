
import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def format_dim_design(design_table):
    '''
    argument:design_table
        type:dict
            key: table name
            value: updated content (list of dictionary)

    return:
        type: list of list
            for each row:
                design_id: id (int)
                design_name:name of design (str)
                file_location:path of file (str)
                file_name:name of file (str)
    raise:
        RuntimeError
        KeyError

    '''
    try:
        # read table content
        content = design_table['design']

        # formatting
        result = []
        for row in content:
            result.append({
                'design_id': row['design_id'],
                'design_name': row['design_name'],
                'file_location': row['file_location'],
                'file_name': row['file_name'],
            })
        return result
    except KeyError as k:
        logger.error(f'Error retrieving data, {k}')

    except Exception as e:
        logger.error(e)
        raise RuntimeError
