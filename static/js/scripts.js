
function computeColor(color){
    return color;
}

function hexToRgb(hex) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);
    return { r, g, b };
}

function rgbToHex(r, g, b) {
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

function mixColors(color1, color2, ratio) {
    let rgb1 = hexToRgb(color1);
    let rgb2 = hexToRgb(color2);

    let mixedR = Math.round(rgb1.r * ratio + rgb2.r * (1 - ratio));
    let mixedG = Math.round(rgb1.g * ratio + rgb2.g * (1 - ratio));
    let mixedB = Math.round(rgb1.b * ratio + rgb2.b * (1 - ratio));

    return rgbToHex(mixedR, mixedG, mixedB);
}

function updateColor(colorName, colorProperty, computedColorProperty, color)
{
    document.documentElement.style.setProperty(colorProperty, color);
    
    // document.documentElement.style.setProperty(computedColorProperty, computeColor(color));
    localStorage.setItem(colorName, color);

}

function applyColors() {
    let c1 = document.getElementById('color1-picker').value;
    let c2 = document.getElementById('color2-picker').value;
    let c3 = document.getElementById('color3-picker').value;

    updateColor('color1', '--color-1', '--color-1-computed', c1)
    updateColor('color2', '--color-2', '--color-2-computed', c2)
    updateColor('color3', '--color-3', '--color-3-computed', c3)

    mixAllColors();
}

function mixAllColors(){

    if(!document.getElementById('color1-picker'))
        return;
    
    if(!document.getElementById('color2-picker'))
        return;
    
    if(!document.getElementById('color3-picker'))
        return;

    let c1 = document.getElementById('color1-picker').value;
    // let c2 = document.getElementById('color2-picker').value;
    let c3 = document.getElementById('color3-picker').value;

    let c133 = mixColors(c1, c3, 0.33);
    let c13 = mixColors(c1, c3, 0.5);
    let c113 = mixColors(c1, c3, 0.66);

    document.documentElement.style.setProperty('--color-133', c133 )
    document.documentElement.style.setProperty('--color-13', c13 )
    document.documentElement.style.setProperty('--color-113', c113 )

    localStorage.setItem('color-133', c133);
    localStorage.setItem('color-13', c13);
    localStorage.setItem('color-113', c113);
    
    console.log("colors changed");
}

function setColor(colorName, alternativeColor, colorObject, colorProperty, computedColorProperty)
{
    var color = localStorage.getItem(colorName) || alternativeColor
    if(document.getElementById(colorObject))
        document.getElementById(colorObject).value = color;
    
    updateColor(colorName, colorProperty, computedColorProperty, color);
    mixAllColors();

    if(document.getElementById(colorObject))
        document.getElementById(colorObject).addEventListener('input', applyColors);
    
}

function onLoad(){
    setColor('color1', '#212529', 'color1-picker', '--color-1', '--color-1-computed')
    setColor('color2', '#ffffff', 'color2-picker', '--color-2', '--color-2-computed')
    setColor('color3', '#64a8f0', 'color3-picker', '--color-3', '--color-3-computed')

    let c1 = localStorage.getItem('color1');
    let c3 = localStorage.getItem('color3');
    
    document.documentElement.style.setProperty('--color-133', localStorage.getItem('color-133') || mixColors(c1, c3, 0.33) )
    document.documentElement.style.setProperty('--color-13', localStorage.getItem('color-13') || mixColors(c1, c3, 0.5) )
    document.documentElement.style.setProperty('--color-113', localStorage.getItem('color-113') || mixColors(c1, c3, 0.66) )
}

document.addEventListener('DOMContentLoaded', () => { onLoad() });