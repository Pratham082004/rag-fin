import re

from app.schemas.parsed_filing import FilingSection

from app.ingestion.patterns import SEC_SECTION_PATTERNS


class SectionExtractor:

    def extract(self, text: str) -> list[FilingSection]:

        matches = []

        upper = text.upper()

        for title, patterns in SEC_SECTION_PATTERNS.items():

            for pattern in patterns:

                m = re.search(pattern, upper)

                if m:

                    matches.append(
                        (
                            m.start(),
                            title,
                        )
                    )

                    break

        matches.sort()

        sections = []

        for i, (start, title) in enumerate(matches):

            if i == len(matches) - 1:

                end = len(text)

            else:

                end = matches[i + 1][0]

            sections.append(

                FilingSection(

                    title=title,

                    content=text[start:end].strip(),
                )
            )

        return sections