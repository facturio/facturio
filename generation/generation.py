from random import randint
from random import choice
from random import choices
# Import des classes
from facturio.classes.invoice_misc import Advance, Article, Invoice, \
                                              Estimate
from facturio.classes.client import Company, Client
from facturio.classes.user import User

def random_firstname():
    """
    Return a random first name from a list
    """
    with open("generation/datasets/firstnames.txt", "r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_lastname():
    """
    Return a random last name from a list
    """
    with open("generation/datasets/lastnames.txt", "r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_address():
    """
    Return a random address from a list
    """
    with open("generation/datasets/adress.txt", "r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_companyname():
    """
    Return a random address from a list
    """
    with open("generation/datasets/companynames.txt","r") as f:
        return choice([n[:-1] for n in f.readlines()])

def random_date():
    """
    Return a random date in Unix format
    """
    with open("generation/datasets/unix_date.txt","r") as f:
        return int(choice([n[:-1] for n in f.readlines()]))


def create_random_articles(nb_articles):
    """
    Return an array of articles
    """
    with open("generation/datasets/articles.txt","r") as f:
        article_list = choices([n[:-1].split('\t') for n in f.readlines()],
        k=nb_articles)
        for i in range(len(article_list)):
            article_list[i] = Article(article_list[i][0],
            float(article_list[i][2]), int(article_list[i][1]),"blank description")
        return article_list

def create_random_advances(nb_advances):
    """
    Return an array of advances
    """
    with open("generation/datasets/advances.txt","r") as f:
        advance_list = choices([n[:-1].split('\t') for n in f.readlines()],
        k=nb_advances)
        for i in range(len(advance_list)):
            advance_list[i] = Advance(float(advance_list[i][0]),
            int(advance_list[i][1]))
        return advance_list


def create_random_phone_number():
    """
    Create randomly a phone number
    """
    phone_number = "0"
    for i in range(9):
        phone_number += str(randint(0,9))
    return phone_number

def create_random_email_address(firstname, lastname):
    """
    Create a mail address from a firstname and last name:
    """
    domain = ["gmail", "laposte", "sfr", "anet", "neuf", "hotmail", "univ-tln"]
    extension = ["fr", "us", "uk", "gr", "jp"]
    return f"{firstname}.{lastname}@.{choice(domain)}.{choice(extension)}"

def create_random_business_number():
    """
    Create randomly a business number
    """
    business_number = ""
    for i in range(16):
        business_number += str(randint(0, 9))
    return business_number

def create_random_client(is_company=True):
    """
    Return a random client
    """
    first_name = random_firstname()
    last_name = random_lastname()
    address = random_address()
    phone_number = create_random_phone_number()
    email = create_random_email_address(first_name, last_name)
    # Procédures différents pour une client particulier
    if(is_company):
        company_name = random_companyname()
        business_number = create_random_business_number()
        return Company(company_name, first_name, last_name, email, address,
                       phone_number, business_number)
    else:
        return Client(first_name, last_name, email, address, phone_number)

def create_random_user():
    """
    Return a random user
    """
    company_name = random_companyname()
    first_name = random_firstname()
    last_name = random_lastname()
    address = random_address()
    phone_number = create_random_phone_number()
    business_number = create_random_business_number()
    email = create_random_email_address(first_name, last_name)
    return User(company_name=company_name,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                phone_number=phone_number,
                business_number=business_number)

def create_random_invoice():
    """
    Return a random invoice
    """

    if User.exists():
        user = User.get_instance()
    else:
        user = create_random_user()
    client = create_random_client()
    articles = create_random_articles(5)
    date = random_date()
    taxes = 0.2
    from random import randint
    amount = randint(0, 1000)
    advances = create_random_advances(2)
    return Invoice(user, client, articles, date, taxes, amount, advances)

def create_random_estimate():
    """
    Return a random estimate
    """
    if User.exists():
        user = User.get_instance()
    else:
        user = create_random_user()
    client = create_random_client()
    articles = create_random_articles(5)
    date = random_date()
    taxes = 0.2
    amount = randint(0, 1000)
    return Estimate(user, client, articles, date, taxes, amount)


if __name__ == "__main__":
    from facturio.db.invoicedao import InvoiceDAO
    from facturio.db.estimatedao import EstimateDAO
    inv = InvoiceDAO.get_instance()
    estimate = EstimateDAO.get_instance()
    for _ in range(30):
        inv.insert(create_random_invoice())
        estimate.insert(create_random_estimate())
