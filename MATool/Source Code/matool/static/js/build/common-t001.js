// Creator : TuandDV

function has_attr_value(element, attr_name) {
  var attr = $(this).attr(attr_name);

  // For some browsers, `attr` is undefined; for others, `attr` is false. Check for both.
  if (typeof attr !== typeof undefined && attr !== false) {
      return true;
  }

  return false;
}