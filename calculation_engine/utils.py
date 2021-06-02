class SimpleCappUtils:
    @classmethod
    def unpack_dict_in_list_of_rows(cls, level_unpack: int, dict_to_unpack: dict) -> list:
        """To unpack dict values in a list of rows"""

        dicts_by_level = {0: dict_to_unpack.values()}
        if level_unpack == 0:
            return list(dicts_by_level[0].values())


        list_to_return = []
        for i in range(level_unpack):
            dicts_by_level[i+1] = []
            for value in dicts_by_level[i]:
                dicts_by_level[i+1].extend(list(value.values()))
                if i < level_unpack-1:
                    continue
                for v in dicts_by_level[i]:
                    if v not in list_to_return:
                        list_to_return.append(v)
        
        return list_to_return


    @classmethod
    def get_unique_values(cls, operations: list, key: str) -> list:
        """To get unique values in list of rows"""
        unique_values = []
        for op in operations:
            if getattr(op, key) not in unique_values:
                unique_values.append(getattr(op, key))
        return unique_values

    @classmethod
    def get_list_with_filters(cls, filter_dict: dict, list_to_filter: list):
        """To execute a simple 'eq' filter in list of rows"""
        result_list = []
        for i in list_to_filter:
            conditions = []
            for k, v in filter_dict.items():
                if i is dict:
                    conditions.append(i[k] == v)
                else:
                    conditions.append(getattr(i, k) == v)
            if not (False in conditions):
                result_list.append(i)

        return result_list

    @classmethod
    def index_list_by_list_of_keys(
        cls, list_to_index: list, list_of_keys: list, key_name: str
    ):
        """To index a list by a list of keys"""
        return {
            key: [i for i in list_to_index if getattr(i, key_name) == key]
            for key in list_of_keys
        }
