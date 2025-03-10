function joinStrings(strings, separator) {
    if (strings == null) {
        return '';
    }
    return strings
        .filter(str => str != null && str !== '')
        .reduce((result, str, index) => {
            if (index === 0) {
                return str;
            }
            return `${result}${separator}${str}`;
        }, '');
}

export { joinStrings };