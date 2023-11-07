import logging

logger = logging.getLogger("format_dim_staff ")
logger.setLevel(logging.INFO)


def format_dim_staff(staff_data):
    """
    formats the data to populate the dim_staff table

    Parameters
    ----------
    json object containing the data from the staff table and department table.

    Raises
    ------
        KeyError if incorrect staff data provided
        Warning if a staff record cannot be formatted correctly

    Returns
    ------
    list of lists
        each list contains the staff_id, first_name,\
        last_name, department, location, email address

    """

    try:
        if "staff" not in staff_data.keys():
            raise KeyError("Incorrect staff data provided")

        staff = [x.copy() for x in staff_data["staff"]]
        department = [x.copy() for x in staff_data["department"]]

        for s in staff:
            for d in department:
                if s["department_id"] == d["department_id"]:
                    s["department"] = d["department_name"]
                    s["location"] = d["location"]

        for s in staff:
            if "department" not in s.keys():
                logger.warning(
                    f"staff_id {s['staff_id']}: no valid department_id "
                )  # noqa E501
                staff.remove(s)

        f_staff = [
            [
                s["staff_id"],
                s["first_name"],
                s["last_name"],
                s["department"],
                s["location"],
                s["email_address"],
            ]
            for s in staff
        ]

        logger.info("dim_staff data formatted sucessfully")
        return f_staff
    except KeyError as e:
        logger.error(f"{e}")
    except AttributeError as e:
        logger.error(f"{e}")
    except Exception as e:
        logger.error(f"An unexpected Error Occured: {e}")
