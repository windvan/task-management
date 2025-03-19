function dateToStr(date) {
  if (date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  } else return null
}

function strToDate(dateStr, format) {
  let date
  switch (format) {
    case 'yyyy-mm-dd':
      date = new Date(dateStr)
      break
    case 'yyyy':
      date = new Date(dateStr, 0)
      break
    case 'yyyy-mm':
      {
        let [yyyy, mm] = dateStr.split('-')
        date = new Date(yyyy, mm)
      }
      break
    default:
      date = new Date(dateStr)
      break
  }

  return date
}

export {dateToStr,strToDate}