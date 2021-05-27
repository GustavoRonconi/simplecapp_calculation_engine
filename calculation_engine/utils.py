class SimpleCappUtils:
    @classmethod
    def get_unique_values(self, operations: list, key: str) -> list:
        """To get unique values in list of rows"""
        unique_values = []
        for op in operations:
            if getattr(op, key) not in unique_values:
                unique_values.append(getattr(op, key))
        return unique_values

    @classmethod
    def get_list_with_filters(self, filter_dict: dict, list_to_filter: list):
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
        self, list_to_index: list, list_of_keys: list, key_name: str
    ):
        """To index a list by a list of keys"""
        return {
            key: [i for i in list_to_index if getattr(i, key_name) == key]
            for key in list_of_keys
        }
