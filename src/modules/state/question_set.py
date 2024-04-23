from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder

#
# default question sets
#

easy_questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What's Tony's last name")
    .add_option("Doan")
    .add_option("Xu")
    .add_option("Huang")
    .add_option("Sheldon")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
    .build(),
    MultipleChoiceQuestionBuilder()
    .add_question("What day is it")
    .add_option("Mon")
    .add_option("Tue")
    .add_option("Wed")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Mon").build())
    .build()
]

demo_questions = [

    MultipleChoiceQuestionBuilder()
    .add_question("Which cities are a capital city of a country?")
    .add_option("Stockholm")
    .add_option("Zurich")
    .add_option("Prague")
    .add_option("Budapest")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Stockholm").add_solution("Prague").add_solution("Budapest").build())
    .build(),

    # MultipleChoiceQuestionBuilder()
    # .add_question("Which term does not belong in the following group?")
    # .add_option("Semaphore")
    # .add_option("Mutex")
    # .add_option("Thread")
    # .add_option("Condition variable")
    # .add_solution(MultipleChoiceSolutionBuilder().add_solution("Thread").build())
    # .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("If 6+4=210, 9+2=711, and 8+5=313, then 5+2=?")
    .add_option("612")
    .add_option("513")
    .add_option("307")
    .add_option("811")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("307").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Are you enjoying the game so far?")
    .add_option("YES!")
    .add_option("NO:((")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("YES!").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("The \"Four Great Inventions\" of ancient China are:")
    .add_option("Paper, Printing, Gunpowerder, Silk")
    .add_option("Compass, Paper, Fireworks, Printing")
    .add_option("Gunpowder, Kites, Printing, Paper")
    .add_option("Paper, Printing, Gunpowder, Compass")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Paper, Printing, Gunpowder, Compass").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which of the following is NOT a correct description of Erlang?")
    .add_option("Originally developed within Ericsson.")
    .add_option("Functional language.")
    .add_option("Created in the 1970s.")
    .add_option("Runs on the BEAM.")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Created in the 1970s.").build())
    .build(),

]

cs_questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What is the purpose of virtual memory in operating systems?")
    .add_option("To allow multiple programs to run simultaneously")
    .add_option("To provide a larger address space than physical memory")
    .add_option("To improve the performance of disk I/O operations")
    .add_option("To protect the operating system from malicious software")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("To provide a larger address space than physical memory").build())
    .build(),


    MultipleChoiceQuestionBuilder()
    .add_question("Which of the following is a key characteristic of the TCP protocol?")
    .add_option("Connectionless communication")
    .add_option("Guaranteed delivery of packets")
    .add_option("Minimal overhead")
    .add_option("Limited scalability")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Guaranteed delivery of packets").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("What is the purpose of the \"fork()\" system call in Unix-like operating systems?")
    .add_option("To create a new process")
    .add_option("To allocate memory for a new process")
    .add_option("To terminate a process")
    .add_option("To wait for a child process to terminate")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("To create a new process").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which sorting algorithm has the best worst-case time complexity?")
    .add_option("Bubble sort")
    .add_option("Quick sort")
    .add_option("Merge sort")
    .add_option("Insertion sort")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Merge sort").build())
    .build(),

]

iq_questions = [
    MultipleChoiceQuestionBuilder()
    .add_question("What comes next in the sequence? 2, 6, 12, 20, ?")
    .add_option("30")
    .add_option("24")
    .add_option("36")
    .add_option("42")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("30").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("If all Feps are Leps, and some Leps are Peps, then some Feps are definitely Peps.")
    .add_option("True")
    .add_option("False")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("False").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("If 6+4=210, 9+2=711, and 8+5=313, then 5+2=?")
    .add_option("612")
    .add_option("513")
    .add_option("307")
    .add_option("811")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("307").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which of these is the largest species of penguin?")
    .add_option("Emperor")
    .add_option("King")
    .add_option("Adelie")
    .add_option("Chinstrap")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Emperor").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which country is the largest producer of coffee in the world?")
    .add_option("Colombia")
    .add_option("Ethiopia")
    .add_option("France")
    .add_option("Brazil")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Brazil").build())
    .build(),

    MultipleChoiceQuestionBuilder()
    .add_question("Which city is not a capital city of a country?")
    .add_option("Zurich")
    .add_option("Prague")
    .add_option("Stockholm")
    .add_option("Budapest")
    .add_solution(MultipleChoiceSolutionBuilder().add_solution("Zurich").build())
    .build(),

]

QUESTIONS = [easy_questions, demo_questions, iq_questions]
QUESTION_NAMES = ["Question Set 1: easy",
                  "Question Set 2: demo",
                  "Question Set 3: IQ"]
NUM_QUESTIONS = len(QUESTIONS)
