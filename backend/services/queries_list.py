from pydantic import UUID4


class QueriesList:
    def get_person_film(self, person_name: str, from_item: int, page_size: int):
        query = {
            "from": from_item,
            "size": page_size,
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match_phrase": {
                                                        "actors_names": person_name
                                                    }
                                                }
                                            ],
                                            "minimum_should_match": 1,
                                        }
                                    },
                                    {
                                        "bool": {
                                            "should": [
                                                {
                                                    "bool": {
                                                        "should": [
                                                            {
                                                                "match_phrase": {
                                                                    "writers_names": person_name
                                                                }
                                                            }
                                                        ],
                                                        "minimum_should_match": 1,
                                                    }
                                                },
                                                {
                                                    "bool": {
                                                        "should": [
                                                            {
                                                                "match_phrase": {
                                                                    "director": person_name
                                                                }
                                                            }
                                                        ],
                                                        "minimum_should_match": 1,
                                                    }
                                                },
                                            ],
                                            "minimum_should_match": 1,
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        }
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
        }
        return query

    def get_person_by_name(self, person_name: str):
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "bool": {
                                "should": [
                                    {"match_phrase": {"full_name": person_name}}
                                ],
                                "minimum_should_match": 1,
                            }
                        }
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
        }

        return query

    def get_person_by_uuid(self, person_id: UUID4):
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "bool": {
                                "should": [{"match_phrase": {"id": person_id}}],
                                "minimum_should_match": 1,
                            }
                        }
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
        }

        return query
