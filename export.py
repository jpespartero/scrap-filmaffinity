import argparse
import requests
import csv
import bs4

from datetime import datetime


def get_date(tag):
    """Gets date from tag (format YYYY-MM-DD)"""
    date_str = tag.string[len("Rated on "):].strip()
    fecha = datetime.strptime(date_str, "%B %d, %Y").date()
    return fecha.strftime("%Y-%m-%d")


def get_directors(tag):
    """Gets directors from a film"""
    directors = list(
        map(
            lambda d: d.a["title"],
            tag.find_all(class_="mc-director")[0].find_all(class_="nb")))

    for director in directors:
        if director.endswith("(Creator)"):
            director = director[:-10]

    return ", ".join(directors)


def is_film(tag):
    """Checks if given tag is a film"""
    title = tag.find_all(class_="mc-title")[0].a.string.strip()
    skip = ["(TV Series)", "(TV Miniseries)", "(TV)", "(S)"]
    return not any(map(title.endswith, skip))


def get_data(user_id):
    """Gets list of films from user id"""
    data = []
    eof = False
    n = 1
    FA = "https://www.filmaffinity.com/en/userratings.php?user_id={id}&p={n}&orderby=4&chv=list"
    print(FA)

    while not eof:
        url = FA.format(id=user_id, n=n)
        print(f"Downloading page: {url}")
        request = requests.get(url)
        request.encoding = "utf-8"
        page = bs4.BeautifulSoup(request.text, "lxml")
        rows = page.find_all("div", class_="row mb-4")
        print(f"  Movie rows found on page: {len(rows)}")

        for row in rows:
            # User rating
            user_rating = ""
            col2 = row.find("div", class_="col-2")
            if col2:
                user_rating_tag = col2.find("div", class_="fa-user-rat-box")
                user_rating = user_rating_tag.get_text(strip=True) if user_rating_tag else ""

            # Movie item
            item = row.find("div", class_="user-ratings-movie-item")
            if not item:
                continue

            # Title
            title_tag = item.find("div", class_="mc-title")
            title = title_tag.get_text(strip=True) if title_tag else "(No title)"
            # Year
            year_tag = item.find("span", class_="mc-year")
            year = year_tag.get_text(strip=True) if year_tag else ""
            # Average rating
            avg_rating_tag = item.find("div", class_="avg mx-0")
            avg_rating = avg_rating_tag.get_text(strip=True) if avg_rating_tag else ""
            # Directors
            directors_tag = item.find("div", class_="mc-director")
            if directors_tag:
                directors = ", ".join([a.get_text(strip=True) for a in directors_tag.find_all("a")])
            else:
                directors = ""
            # Actors (mc-credits)
            actors_tag = item.find("div", class_="mc-cast")
            if actors_tag:
                actors = actors_tag.get_text(strip=True)
            else:
                actors = ""

            print(f"    Title: {title} | Year: {year} | User Rating: {user_rating} | Avg Rating: {avg_rating} | Directors: {directors} | Actors: {actors}")

            film = {
                "Title": title,
                "Year": year,
                "UserRating": user_rating,
                "AvgRating": avg_rating,
                "Directors": directors,
                "Actors": actors
            }
            data.append(film)

        eof = request.status_code != 200 or len(rows) == 0
        if not eof:
            print(f"Page {n}", end="\r")
        else:
            print(f"Page {n-1}. Download complete!")

        n += 1

    return data


def save_to_csv(data, filename):
    """Saves list of dictionaries in a csv file"""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(data[0]))
        for film in data:
            writer.writerow(list(film.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "Generates csv compatible with LetterBoxd from Filmaffinity user's id.")
    parser.add_argument("id", help="User's id")
    parser.add_argument(
        "--csv", nargs=1, help="Name of export FILE", metavar="FILE")

    args = parser.parse_args()
    export_file = args.csv[0] if args.csv else f"filmAffinity_{args.id}.csv"

    try:
        data = get_data(args.id)
        print(data)
    except ValueError as v:
        print("Error:", v)
        exit()

    save_to_csv(data, export_file)