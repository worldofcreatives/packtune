from app.models import db, Audio, environment, SCHEMA
from sqlalchemy.sql import text


def seed_audio():
    audio = [
        Audio(
            title="Bob Marley: One Love",
            description="The story of how reggae icon Bob Marley overcame adversity, and the journey behind his revolutionary music.",
            genre="Drama",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/bob-marley-thumbnail.jpeg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/bob+marley.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/bob+marley.mp3",
            user_id=1,
        ),
        Audio(
            title="Godzilla and Kong",
            description="The epic next chapter in the cinematic Monsterverse pits two of the greatest icons in motion picture history against each other--the fearsome Godzilla and the mighty Kong--with humanity caught in the balance.",
            genre="Action",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/godzilla-kong-thumbnail.jpeg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/godzilla+and+kong.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/godzilla+and+kong.mp3",
            user_id=2,
        ),
        Audio(
            title="Moana",
            description="In ancient Polynesia, when a terrible curse incurred by the demigod Maui reaches Moana's island, she answers the Ocean's call to seek out Maui to set things right.",
            genre="Fantasy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/moana-thumbnail.jpeg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/moana.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/moana.mp3",
            user_id=3,
        ),
        Audio(
            title="A Quiet Place",
            description="A family struggles for survival in a world where most humans have been killed by blind but noise-sensitive creatures. They are forced to communicate in sign language to keep the creatures at bay.",
            genre="Horror",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/quiet-place-thumbnail.jpeg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/quiet+place.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/quiet+place.mp3",
            user_id=4,
        ),
        Audio(
            title="Spaceman",
            description="Jakub Procházka, orphaned as a boy and raised in the Czech countryside by his grandparents, overcomes his odds to become the country's first astronaut.",
            genre="Comedy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/spaceman-thumbnail.jpeg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/spaceman.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/spaceman.mp3",
            user_id=5,
        ),
        Audio(
            title="Asteroid City",
            description="Following a writer on his world famous fictional play about a grieving father who travels with his tech-obsessed family to small rural Asteroid City to compete in a junior stargazing event, only to have his world view disrupted forever.",
            genre="Drama",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/asteroid-city.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=1,
        ),
        Audio(
            title="Elemental",
            description="Follows Ember and Wade, in a city where fire-, water-, earth- and air-residents live together.",
            genre="Fantasy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/elemental.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=2,
        ),
        Audio(
            title="Guardians of the Galaxy",
            description="Still reeling from the loss of Gamora, Peter Quill rallies his team to defend the universe and one of their own - a mission that could mean the end of the Guardians if not successful.",
            genre="Action",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/guardians.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=3,
        ),
        Audio(
            title="Indiana Jones",
            description="In 1935, Indiana Jones is tasked by Indian villagers with reclaiming a rock stolen from them by a secret cult beneath the catacombs of an ancient palace.",
            genre="Horror",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/indiana-jones.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=4,
        ),
        Audio(
            title="Little Mermaid",
            description="A young mermaid makes a deal with a sea witch to trade her beautiful voice for human legs so she can discover the world above water and impress a prince.",
            genre="Comedy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/littlemermaid.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=5,
        ),
        Audio(
            title="Spiderman",
            description="Teen Miles Morales becomes the Spider-Man of his universe and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
            genre="Drama",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/spiderman.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=1,
        ),
        Audio(
            title="Ruby Gillman, Teenage Kraken",
            description="A shy adolescent learns that she comes from a fabled royal family of legendary sea krakens and that her destiny lies in the depths of the waters, which is bigger than she could have ever imagined.",
            genre="Action",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/teen-kraken.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=2,
        ),
        Audio(
            title="Transformers",
            description="In ancient Polynesia, when a terrible curse incurred by the demigod Maui reaches Moana's island, she answers the Ocean's call to seek out Maui to set things right.",
            genre="Fantasy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/transformers.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=3,
        ),
        Audio(
            title="No Hard Feelings",
            description="On the brink of losing her home, Maddie finds an intriguing job listing: helicopter parents looking for someone to bring their introverted 19-year-old son out of his shell before college. She has one summer to make him a man or die trying.",
            genre="Horror",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/hard-feelings.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=4,
        ),
        Audio(
            title="The Flash",
            description="Barry Allen uses his super speed to change the past, but his attempt to save his family creates a world without super heroes, forcing him to race for his life in order to save the future.",
            genre="Comedy",
            thumbnail_url="https://indieroll-bucket.s3.us-east-2.aaa.com/the-flash.jpg",
            video_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp4",
            audio_url="https://indieroll-bucket.s3.us-east-2.aaa.com/test-movie.mp3",
            user_id=5,
        ),
    ]

    db.session.add_all(audio)
    db.session.commit()
    print("Files seeded")


def undo_audio():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.audio_content RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM audio_content"))

    db.session.commit()
