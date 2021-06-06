class UnpackError(BaseException):
    pass


class SimpleCappUtils:
    @classmethod
    def unpack_dict_in_list_of_rows(
        cls, level_unpack: int, dict_to_unpack: dict
    ) -> list:
        """To unpack dict values in a list of rows (only dicts os dicts)"""

        dicts_by_level = {0: dict_to_unpack.values()}
        if level_unpack == 0:
            return list(dicts_by_level[0].values())

        list_to_return = []
        for i in range(level_unpack):
            dicts_by_level[i + 1] = []
            for value in dicts_by_level[i]:
                if type(value) is str:
                    raise UnpackError("The level is so much high to unpack")
                dicts_by_level[i + 1].extend(list(value.values()))
                if i < level_unpack - 1:
                    continue
                for v in dicts_by_level[i]:
                    if v not in list_to_return:
                        list_to_return.append(v)

        return list_to_return

    @classmethod
    def get_unique_values(cls, list_to_verify: list, key: str) -> list:
        """To get unique values (to especific key) in list of rows"""
        unique_values = []
        for i in list_to_verify:
            if type(i) is dict:
                condition, value = i[key] not in unique_values, i[key]
            else:
                condition, value = getattr(i, key) not in unique_values, getattr(i, key)
            if condition:
                unique_values.append(value)
        return unique_values

    @classmethod
    def get_list_with_filters(cls, filter_dict: dict, list_to_filter: list) -> list:
        """To execute a simple 'eq' filter in list of rows"""
        result_list = []
        for i in list_to_filter:
            conditions = []
            for k, v in filter_dict.items():
                if type(i) is dict:
                    conditions.append(i[k] == v)
                else:
                    conditions.append(getattr(i, k) == v)
            if not (False in conditions):
                result_list.append(i)

        return result_list

    @classmethod
    def index_list_by_list_of_keys(
        cls, list_to_index: list, list_of_keys: list, key_name: str
    ) -> dict:
        """To index a list by a list of keys"""
        return {
            key: SimpleCappUtils.get_list_with_filters({key_name: key}, list_to_index)
            for key in list_of_keys
        }
