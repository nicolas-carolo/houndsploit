from HoundSploit.searcher.utils.constants import BASE_PATH
from HoundSploit.searcher.utils.file import check_file_existence

bookmarks_csv_header = "vulnerability_id,vulnerability_class,date\n"
suggestions_csv_header = "searched,suggestion,autoreplacement\n"
bookmarks_csv_file = BASE_PATH + "bookmarks.csv"
suggestions_csv_file = BASE_PATH + "custom_suggestions.csv"


def add_bookmark_to_csv(vulnerability_id, vulnerability_class, date):
    new_record = vulnerability_id + "," + vulnerability_class + ",\"" + str(date) + "\"\n"
    add_record_to_csv(bookmarks_csv_file, bookmarks_csv_header, new_record)


def add_suggestion_to_csv(searched, suggestion, autoreplacement):
    new_record = searched + "," + suggestion + "," + autoreplacement + "\n"
    add_record_to_csv(suggestions_csv_file, suggestions_csv_header, new_record)


def add_record_to_csv(csv_file, csv_header, new_record):
    if not check_file_existence(csv_file):
        f= open(csv_file, "w+")
        f.write(csv_header)
        f.close()
    f= open(csv_file, "a+")
    f.write(new_record)
    f.close()


def delete_bookmark_from_csv(vulnerability_id, vulnerability_class):
    record_to_be_deleted = vulnerability_id + "," + vulnerability_class
    delete_record_from_csv(bookmarks_csv_file, bookmarks_csv_header, record_to_be_deleted)


def delete_suggestion_from_csv(searched):
    record_to_be_deleted = searched
    delete_record_from_csv(suggestions_csv_file, suggestions_csv_header, record_to_be_deleted)


def delete_record_from_csv(csv_file, csv_header, record_to_be_deleted):
    with open(csv_file, "r") as f:
        lines = f.readlines()
    f= open(csv_file, "w+")
    f.write(csv_header)
    f.close()
    with open(csv_file, "a+") as f:
        for line in lines[1:]:
            if not line.startswith(record_to_be_deleted):
                f.write(line)


def edit_suggestion_in_csv(searched, suggestion, autoreplacement):
    delete_suggestion_from_csv(searched)
    add_suggestion_to_csv(searched, suggestion, autoreplacement)
