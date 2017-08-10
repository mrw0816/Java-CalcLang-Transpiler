# Java-CalcLang-Transpiler

-------------------------------------------------------
CalcLang Context free grammar:  (E = expression) 

statements -> statement

statements -> statement statements

statement -> V = E

statement -> SHOW E           (show)

statement -> MESSAGE STRING   (keyword is "msg")

statement -> INPUT STRING V      (STRING is the token for a "whatever")

statement -> NEWLINE          (newline)

(use E instead of <expression>, etc.)

E -> T
E -> T + E | T - E

T -> F
T -> F * T | F / T

F -> N    (from lexical phase:  number)
F -> V    (from lexical phase:  variable)
F -> (E)
F -> - F
F -> BIFN (E)
------------------------------------------------------------
