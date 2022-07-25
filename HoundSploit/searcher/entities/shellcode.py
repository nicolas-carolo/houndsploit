from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_
from sqlalchemy.ext.declarative import declarative_base
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list, void_result_set
from HoundSploit.searcher.utils.vulnerability_filter import filter_vulnerabilities_without_comparator, filter_vulnerabilities_with_comparator
from HoundSploit.searcher.utils.vulnerability import get_software_name_and_version_number, get_software_name_and_version_number_word_lists,\
    filter_vulnerability_based_on_version
from HoundSploit.searcher.utils.string import str_contains_num_version, str_contains_software_name_and_num_version
from HoundSploit.searcher.utils.list import join_lists

Base = declarative_base()

N_MAX_RESULTS_NUMB_VERSION = 20000


class Shellcode(Base):
    __tablename__ = 'searcher_shellcode'

    id = Column(Integer, primary_key=True)
    file = Column(String)
    description = Column(String)
    date = Column(String)
    author = Column(String)
    type = Column(String)
    platform = Column(String)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __init__(self, id, file, description, date, author, shellcode_type, platform):
        self.id = id
        self.file = file
        self.description = description
        self.date = date
        self.author = author
        self.type = shellcode_type
        self.platform = platform


    @staticmethod
    def search(searched_text):
        word_list = str(searched_text).split()
        if str(searched_text).isnumeric():
            return Shellcode.search_numerical(word_list[0])
        elif str_contains_software_name_and_num_version(searched_text):
            result_set = Shellcode.search_based_on_software_version(word_list)
            # union with standard research
            std_result_set = Shellcode.search_based_on_searchbox(word_list)
            union_result_set = join_lists(result_set, std_result_set)
            if len(union_result_set) > 0:
                return union_result_set
            else:
                return Shellcode.search_based_on_description(word_list)
        else:
            result_set = Shellcode.search_based_on_description(word_list)
            if len(result_set) > 0:
                return result_set
            else:
                result_set = Shellcode.search_based_on_file_name(word_list)
                if len(result_set) > 0:
                    return result_set
                else:
                    return Shellcode.search_based_on_author(word_list)


    @staticmethod
    def search_numerical(searched_text):
        session = start_session()
        queryset = session.query(Shellcode).filter(or_(Shellcode.description.contains(searched_text),
                                                    Shellcode.id == int(searched_text),
                                                    Shellcode.file.contains(searched_text)
                                                    ))
        session.close()
        return queryset2list(queryset)


    @staticmethod
    def search_based_on_software_version(word_list):
        software_name, num_version = get_software_name_and_version_number(word_list)
        session = start_session()
        queryset = session.query(Shellcode).filter(and_(Shellcode.description.contains(software_name)))
        query_result_set = queryset2list(queryset)
        session.close()
        # limit the time spent for searching useless results.
        if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
            return void_result_set()
        final_result_set = []
        for shellcode in query_result_set:
            # if shellcode not contains '<'
            if not str(Shellcode.description).__contains__('<'):
                final_result_set = filter_vulnerabilities_without_comparator(shellcode, num_version, software_name, final_result_set)
            # if shellcode contains '<'
            else:
                final_result_set = filter_vulnerabilities_with_comparator(shellcode, num_version, software_name, final_result_set)
        queryset2list(final_result_set)
        return final_result_set


    @staticmethod
    def search_based_on_searchbox(word_list):
        software_name_word_list, numeric_word_list = get_software_name_and_version_number_word_lists(word_list)
        try:
            session = start_session()
            queryset = session.query(Shellcode).filter(and_(Shellcode.description.contains(word) for word in software_name_word_list))
            session.close()
            query_result_set = queryset2list(queryset)
        except TypeError:
            query_result_set = void_result_set()
        try:
            final_result_set = filter_vulnerability_based_on_version(query_result_set, numeric_word_list)
        except TypeError:
            pass
        queryset2list(final_result_set)
        return final_result_set


    @staticmethod
    def search_based_on_description(word_list):
        session = start_session()
        queryset = session.query(Shellcode).filter(and_(Shellcode.description.contains(word) for word in word_list))
        session.close()
        return queryset2list(queryset)


    @staticmethod
    def search_based_on_file_name(word_list):
        session = start_session()
        queryset = session.query(Shellcode).filter(and_(Shellcode.file.contains(word) for word in word_list))
        session.close()
        return queryset2list(queryset)


    def search_based_on_author(word_list):
        session = start_session()
        queryset = session.query(Shellcode).filter(and_(Shellcode.author.contains(word) for word in word_list))
        session.close()
        return queryset2list(queryset)