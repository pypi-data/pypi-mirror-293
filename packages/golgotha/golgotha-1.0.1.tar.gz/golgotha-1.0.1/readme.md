🔣💀
GOLGOTHA: Define new operators in any language. Do it, coward! Do it now!

(Project status: I consider this project essentially complete and finished, though it may contain minor surprising edge cases and perhaps even bugs. I don't intend to work on this project any more unless to correct those if they are brought to my attention. Also, I don't expect anyone, including myself, to ever use this project again, because I suspect it isn't worth the trouble it may invite. However, who can say?)

Golgotha is a preprocessor for source texts that allows you to define new infix (or prefix or postfix) operators using rules like this:

🔣1$2🔜2-1

This example would result in all statements like a$b being transformed to b-a.

This is mostly useful for rules like:

🔣1⋅2🔜1.dot(2)

in languages that don't support the correct operators you want.

Most of the time, you'll want the golgotha rule to be as small as possible, and just perform the syntactic sugar transform to a function call defined elsewhere.

All Golgotha rules must start on a new line, and begin with 🔣. They are terminated by a newline as well. Other whitespace is not stripped, although the golgotha rule will be interpreted as though each argument may be surrounded by arbitrary amounts of whitespace, which follow them through transformations. Arguments are represented in the rules by numbers (strings of contiguous numerical digit characters [0-9]).

Note that the whitespace-retention rules can be initially counter-intuitive. For example, with a rule like 🔣1$2🔜2-1 as before, the sentence "I gave him x$y apples" would become "I gave himy - xapples"; there is whitespace after the x and before the y in the sentence, and so the same thing happens in the result. (Similar to that old observation that )(() is a palindrome but ()() is not — if you agree with that definition of palindrome, I guess.) meanwhile, the rule 🔣 1$2 🔜 2-1  would produce "I gave him y-x apples", but then "I gave him (x$y) apples" is out of luck...

Golgotha processing of the source text is double-pass, so Golgotha rules are applied in the source text even before they are specified in the text. However, Golgotha rules are still applied in the ORDER they are specified, so you should put more specific forms first such that they are applied before more general forms. If you have both a $ and a $= operator, specify the $= first.

Golgotha takes multiple files (and/or stdin, which outputs to stdout); however, the rules from each file are isolated to it.

Golgotha has no concept of precedence. This is because it is permissible to apply Golgotha rules to a language text that already has infix operators, and we don't want you to have to respecify those to get correct precedence behavior overall. Therefore all transformations must be fully parenthesized, unless you want the default behavior, which is just always operating on the closest "word" strings. Golgotha has an inherent idea of what characters parenthesize in the sense above. These "parenthors" are (), [], and {}.

In classic applications, word characters would be defined as the alphanumerounderscorics. However, since we live in the future, they're probably actually defined as anything Unicode thinks of as a letter, a digit, or a connector (which includes underscores). For convenience, Golgotha also includes "." as a word character, due to the popularity of that character as the "dot" member access operator (not to be confused with any "dot" scalar product operator), so that eg person1.name ∘ person2.name operates on both of those entities as intended, and not on "name" and "person2" alone.

Golgotha does not recognize strings or quotation marks in any particular way. Hypothetically, I could have introduced the concept of quothors to deal with this, possibly using the character 🆀 to define them, but I chose not to because capturing the proper behavior of string escaping was too finicky and bespoke. However, it's a good candidate for if you were to include Golgotha as a language-aware processing pass in a compiler (this would be known as Your Language's golgotha or Your Compiler's golgotha—this is Golgotha's golgotha, or The Golgotha That Belongs To No One), or for Golgotha+. So, long story short: strings will be processed as plain text. You must surround them with parenthors and make sure unbalanced parenthors in strings don't mess things up.

Golgotha has been engineered to be easy to implement more than anything else. The current implementation is in Python 3. But a faster implementation would probably be easy to make in another language, and probably should be made before Golgotha is integrated into your build pipeline.

Golgotha reads files in UTF-8 outputs in UTF-8. It reads files of any line-termination style (the exact bounds on this are some python implementation details I don't know offhand) and outputs files as LF (not CRLF) line-terminated. As God intended. (I would support both, but that was too much bother.)

Implicitly, we just assume you don't want to deal with any Golgotha rule symbols (🔣🔜) in the non-Golgotha parts of your program. There is currently no explicit mechanism to deal with that. However, Golgotha symbols on lines not beginning with 🔣 will be ignored, so it's a constrained edge case.

Golgotha+ is an UNIMPLEMENTED extension to Golgotha which would allow one to set the word character set with 🔠 lines (default 🔠ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_ except actually the default would be Unicode \w behavior probably, which would be much harder to replicate with a 🔠 line); the argument (in 🔣 rule lines) character set with 🔢 lines (default 0123456789); and the set of parenthors with 🅿🔚 lines (default 🅿(🔚), 🅿[🔚], and 🅿{🔚}). I was going to implement Golgotha+ but then I realized that no one was going to use this software anyway so the use case was literally 0. An instance of Golgotha with Golgotha+ rules applied to overwrite defaults may be called a Golgothoid.

Golgotha is intentionally non-Turing-complete. While Golgotha exposes powerful rewrite rules, and a Golgotha line can be generated from text input using a Golgotha rule, Golgotha rules generated this way are not adopted by the Golgotha preprocessor. However, it would be trivial to invoke Golgotha on a text file in some kind of infinite loop, if you were crazy or something. You could even make it diff the input and output each time, and only continue if they were different. And then you would have, like, lambda calculus. There is no reason to do that.

This Golgotha (name picked at random) is not to be confused with the R Natural Language Processing package Golgotha https://github.com/bnosac/golgotha nor the video game / game engine Golgotha https://github.com/videogamepreservation/golgotha / https://github.com/pgrawehr/golgotha

The slogan of this Golgotha is "Because Jesus died for your syn... tax", but this thoroughly lame pun was considered well after the name was finalized.

This project is available both on GitHub and PyPi

GitHub: https://github.com/wyattscarpenter/golgotha

PyPi: https://pypi.org/project/golgotha/
