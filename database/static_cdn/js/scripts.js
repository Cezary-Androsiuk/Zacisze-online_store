function changeColors(primary, secondary, tertiary) {
    document.documentElement.style.setProperty('--primary-color', primary);
    document.documentElement.style.setProperty('--secondary-color', secondary);
    document.documentElement.style.setProperty('--tertiary-color', tertiary);
    document.documentElement.style.setProperty('--background-color', primary);

    const primaryLight = lightenColor(primary, 20);
    const secondaryLight = lightenColor(secondary, 20);
    const tertiaryLight = lightenColor(tertiary, 20);

    document.documentElement.style.setProperty('--primary-light', primaryLight);
    document.documentElement.style.setProperty('--secondary-light', secondaryLight);
    document.documentElement.style.setProperty('--tertiary-light', tertiaryLight);

    localStorage.setItem('primaryColor', primary);
    localStorage.setItem('secondaryColor', secondary);
    localStorage.setItem('tertiaryColor', tertiary);
}

function lightenColor(color, percent) {
    const num = parseInt(color.slice(1), 16),
          amt = Math.round(2.55 * percent),
          R = (num >> 16) + amt,
          G = (num >> 8 & 0x00FF) + amt,
          B = (num & 0x0000FF) + amt;
    return `#${(0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 + (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1).toUpperCase()}`;
}

function applyColors() {
    const primaryColor = document.getElementById('primary-color').value;
    const secondaryColor = document.getElementById('secondary-color').value;
    const tertiaryColor = document.getElementById('tertiary-color').value;
    changeColors(primaryColor, secondaryColor, tertiaryColor);
}

document.addEventListener('DOMContentLoaded', () => {
    if(localStorage)
    {
        console.log("local storage exist")
    }
    else
    {
        console.log("local storage NOT exist")
    }
    const primaryColor = localStorage.getItem('primaryColor') || '#3498db';
    const secondaryColor = localStorage.getItem('secondaryColor') || '#2ecc71';
    const tertiaryColor = localStorage.getItem('tertiaryColor') || '#e74c3c';

    document.getElementById('primary-color').value = primaryColor;
    document.getElementById('secondary-color').value = secondaryColor;
    document.getElementById('tertiary-color').value = tertiaryColor;

    changeColors(primaryColor, secondaryColor, tertiaryColor);

    document.getElementById('primary-color').addEventListener('input', applyColors);
    document.getElementById('secondary-color').addEventListener('input', applyColors);
    document.getElementById('tertiary-color').addEventListener('input', applyColors);
});