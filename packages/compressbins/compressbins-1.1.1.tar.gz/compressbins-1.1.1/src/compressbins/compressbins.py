def compress_bins(bins: list) -> list:
    """
    Convert numpy bins of the form [0,2,4,6,8,10] to a string format ideal for frequency chart tables ['0-2','2-4','4-6','6-8','8-10'].
    :param bins: the bins you want to compress. Must be a list with at least 2 elements Ex) you might pass the bins returned by numpy.histogram()
    :return: List containing the stringified bins expressed as ranges.
    """
    if (not isinstance(bins, list)) or (len(bins) < 2):
        raise ValueError("bins must be an array of length >= 2")
    string_bins = []
    for i in range(len(bins) - 1):
        string_bins.append(str(bins[i]) + '-' + str(bins[i+1]))
    return string_bins
