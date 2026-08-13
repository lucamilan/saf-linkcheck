# 005 · GitHub-style anchors: slugs from headings, accents preserved, with a standard library regex

- **Status:** accepted
- **Date:** 2026-08-09

The #section fragment of an internal link is compared against the anchors derived from the ATX headings of the target file, with GitHub's algorithm: lowercase, punctuation removed, spaces into hyphens, accents preserved, duplicates with a -1/-2 suffix. Why: it is what the real renderer produces — a link that passes the check works there too; and it stays implementable with a standard library regex, extending the parser-free approach of [[decision:002]]. Accepted and declared limits: explicit HTML anchors (<a id=...>) and same-file fragments stay out of scope.

## Relations
- extends → [[decision:002]]
- delivered-by → [[iteration:005]]
