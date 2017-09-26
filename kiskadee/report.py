from abc import ABCMeta, abstractmethod

class Report:
    __metaclass__ = ABCMeta

    def __init__(self, results):
        self.results = results

    @abstractmethod
    def compute_reports(self, results): pass


class CppCheckReport(Report):

    def compute_reports(self):
        result_dict = {
                'warning': 0,
                'error': 0,
                'style': 0
        }
        for result in self.results:
            if 'severity' in list(result.keys()):
                result_dict[result['severity']] += 1
            else:
                print('deu ruimmmm')

        print(result_dict)
        return result_dict

