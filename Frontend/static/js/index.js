async function getDataForEachNum() {
    let reloadtoAnotherSite = await fetch("/data", {
          method: 'GET',
      })
      .then(response => response.json())
      .catch(err => console.error(err))
      window.location.replace("./"+'data');
}