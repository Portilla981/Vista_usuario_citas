// función de habilitar o deshabilitar los campos para editar

function habilitarEdicion(){
const habilitar = document.querySelectorAll('input, select, textarea');

habilitar.forEach(habilitar =>{
    habilitar.removeAttribute('readonly');
    habilitar.removeAttribute('disable');
});

document.getElementsByClassName('btn-guardar').style.display = 'inline-block';
document.querySelector('button[onclick="habilitarEdicion()"]').style.display = 'none';
}