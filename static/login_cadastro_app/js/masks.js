/**
 * Máscaras e validações para campos numéricos
 */

// Máscara para CPF: 000.000.000-00
function maskCPF(input) {
    let value = input.value.replace(/\D/g, ''); // Remove tudo que não é número
    
    if (value.length > 11) {
        value = value.slice(0, 11); // Limita a 11 dígitos
    }
    
    // Formata automaticamente
    if (value.length <= 3) {
        input.value = value;
    } else if (value.length <= 6) {
        input.value = value.slice(0, 3) + '.' + value.slice(3);
    } else if (value.length <= 9) {
        input.value = value.slice(0, 3) + '.' + value.slice(3, 6) + '.' + value.slice(6);
    } else {
        input.value = value.slice(0, 3) + '.' + value.slice(3, 6) + '.' + value.slice(6, 9) + '-' + value.slice(9);
    }
}

// Máscara para Data de Nascimento: dd/mm/aaaa
function maskDate(input) {
    let value = input.value.replace(/\D/g, ''); // Remove tudo que não é número
    
    if (value.length > 8) {
        value = value.slice(0, 8); // Limita a 8 dígitos
    }
    
    // Formata automaticamente
    if (value.length <= 2) {
        input.value = value;
    } else if (value.length <= 4) {
        input.value = value.slice(0, 2) + '/' + value.slice(2);
    } else {
        input.value = value.slice(0, 2) + '/' + value.slice(2, 4) + '/' + value.slice(4);
    }
}

// Máscara para Telefone: (11) 99999-9999
function maskPhone(input) {
    let value = input.value.replace(/\D/g, ''); // Remove tudo que não é número
    
    if (value.length > 11) {
        value = value.slice(0, 11); // Limita a 11 dígitos
    }
    
    // Formata automaticamente
    if (value.length <= 2) {
        input.value = value;
    } else if (value.length <= 7) {
        input.value = '(' + value.slice(0, 2) + ') ' + value.slice(2);
    } else {
        input.value = '(' + value.slice(0, 2) + ') ' + value.slice(2, 7) + '-' + value.slice(7);
    }
}

// Inicializa as máscaras quando o documento carrega
document.addEventListener('DOMContentLoaded', function() {
    const cpfInput = document.getElementById('cpf');
    const dataInput = document.getElementById('data_nascimento');
    const telefoneInput = document.getElementById('telefone');
    
    if (cpfInput) {
        cpfInput.addEventListener('input', function() {
            maskCPF(this);
        });
    }
    
    if (dataInput) {
        dataInput.addEventListener('input', function() {
            maskDate(this);
        });
    }
    
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function() {
            maskPhone(this);
        });
    }
});
