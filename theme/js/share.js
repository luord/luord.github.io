const shareLink = document.querySelector('#addtoanylink');

shareLink.addEventListener('click', async (event) => {
  if (!navigator?.canShare)
    return;

  try {
    await navigator.share(shareConfig);
    shareLink.textContent = 'Shared!';
    event.preventDefault();
  } catch (error) {
    console.error('Sharing failed:', error);
  }
});
