from random import randint
from random import choice
from random import choices
# Import des classes
from facturio.classes.invoice_misc import Advance, Article, Invoice, \
                                              Estimate
from facturio.classes.client import Company, Client
from facturio.classes.user import User

def random_firstname()->str:
    """
    Return a random first name from a list
    """
    with open("datasets/firstnames.txt","r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_lastname()->str:
    """
    Return a random last name from a list
    """
    with open("datasets/lastnames.txt","r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_adress()->str:
    """
    Return a random adress from a list
    """
    with open("datasets/adress.txt","r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_companyname()->str:
    """
    Return a random adress from a list
    """
    with open("datasets/companynames.txt","r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_articles(nb_articles: int):
    """
    Return an array of arrays containing article information
    """
    with open("datasets/articles.txt","r") as f:
        article_list = choices([n[:-1].split('\t') for n in f.readlines()],
        k=nb_articles)
        for i in range(len(article_list)):
            article_list[i] = [article_list[i][0],"blank description",
            float(article_list[i][2]), int(article_list[i][1])]
        return article_list

def random_advances(nb_advances: int):
    """
    Return an array of arrays containing advances information
    """
    with open("datasets/advances.txt","r") as f:
        advance_list = choices([n[:-1].split('\t') for n in f.readlines()],
        k=nb_advances)
        for i in range(len(advance_list)):
            advance_list[i] = [float(advance_list[i][0]),
            int(advance_list[i][1])]
        return advance_list


def create_phone_numer() ->str:
    """
    Create randomly a phone number
    """
    phone_number = "0"
    for i in range(9):
        phone_number += str(randint(0,9))
    return phone_number

def create_email_adress(firstname: str, lastname: str) -> str:
    """
    Create a mail adress from a firstname and last name:
    """
    domain = ["gmail", "laposte", "sfr", "anet", "neuf", "hotmail", "univ-tln"]
    extension = ["fr", "us", "uk", "gr", "jp"]
    return f"{firstname}.{lastname}@.{choice(domain)}.{choice(extension)}"

def create_buisness_number() -> str:
    """
    Create randomly a buisness number
    """
    buisness_number = ""
    for i in range(17):
        buisness_number += str(randint(0,9))
    return buisness_number

def create_client(is_company: bool = True):
    """
    Return an array containing client information
    """
    first_name = random_firstname()
    last_name = random_lastname()
    adress = random_adress()
    phone_number = create_phone_numer()
    email = create_email_adress(first_name, last_name)
    # Procédures différents pour une client particulier
    if(is_company):
        company_name = random_companyname()
        buisness_number = create_buisness_number()
        return [company_name, first_name, last_name, email, adress,
        phone_number, buisness_number]
    else:
        return [first_name, last_name, email, adress, phone_number]

if __name__ == "__main__":
    print()
    print(random_articles(5))
    print()
    print(random_advances(5))
    print()
