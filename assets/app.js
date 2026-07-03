
(() => {
  const picker=document.querySelector('.language');
  const button=document.querySelector('.lang-button');
  if(button){button.addEventListener('click',()=>picker.classList.toggle('open'));document.addEventListener('click',e=>{if(!picker.contains(e.target))picker.classList.remove('open')})}
  document.querySelector('[data-year]').textContent=new Date().getFullYear();
})();
