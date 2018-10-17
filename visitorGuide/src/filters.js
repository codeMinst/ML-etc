import momentjs from 'moment'

export const moment = (date, format) => {
  format = format || 'YYYY-MM-DD hh:mm';
  return momentjs(date).format(format);
};
