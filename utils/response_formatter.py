def format_response(answer, mode):

    if mode == "Concise":

        return answer[:400]

    return answer