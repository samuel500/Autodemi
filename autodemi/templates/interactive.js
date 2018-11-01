function contentInteraction(buttonId, contentId)
{
  button = document.getElementById(buttonId);
  var request = new XMLHttpRequest();
  request.onreadystatechange = function()
  {
    if (request.readyState == 4)
    {
      if (request.status != 200)
      {
        //if server returns error, revert button backround color
        if (button.classList.contains('content-library-button-unselected'))
        {
          button.classList.remove('content-library-button-unselected');
          button.classList.add('content-library-button-selected');
        }
        else
        {
          button.classList.remove('content-library-button-selected');
          button.classList.add('content-library-button-unselected');
        }
      }
      else
      {
        var response = JSON.parse(request.responseText);
        if(response['message'] === 'redirect'){
          window.location.replace(response['target']);
        }
        else {
          for(var bName in response['interactions']){
            currButton = document.getElementById(bName+response['button_context'])
            if (!currButton.classList.contains(response['interactions'][bName])){
              currButton.classList.remove('content-library-button-selected');
              currButton.classList.remove('content-library-button-unselected');
              currButton.classList.add(response['interactions'][bName]);
            }


          }
        }
      }
    }
  }

  if (button.classList.contains('content-library-button-unselected'))
  {
    button.classList.remove('content-library-button-unselected');
    button.classList.add('content-library-button-selected');
  }
  else
  {
    button.classList.remove('content-library-button-selected');
    button.classList.add('content-library-button-unselected');
  }

  request.open('POST', '/content/user_interaction');
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var interactionInfo = 'button_id='+buttonId+'&content_id='+contentId ;
  request.send(interactionInfo);

  return false;
}


function deleteContent(contentId)
{
  var request = new XMLHttpRequest();
  request.onreadystatechange = function()
  {
    if (request.readyState == 4)
    {
      if (request.status != 200)
      {

      }
      else
      {
        var response = JSON.parse(request.responseText)
        if(response['message'] === 'redirect'){
          window.location.replace(response['target']);
        }
        else {
          var response = JSON.parse(request.responseText);
          if(response['message'] === 'redirect'){
            window.location.reload(true);
         }

        }
      }
    }
  }

  request.open('POST', '/content/delete');
  request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var interactionInfo = 'content_id='+contentId;
  request.send(interactionInfo);

  return false;

}
