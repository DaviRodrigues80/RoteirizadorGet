var mapa;
var autocomplete;
var marcadores = []; // Array para armazenar os marcadores


function initMap() {
    if (typeof google !== 'undefined' && google.maps) {
        // Tenta obter a localização do usuário...
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                
                // Obtém as coordenadas da localização do usuário...
                var userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // Configurações do mapa
                    
                

                // Cria o mapa usando Google Maps e centraliza na localização do usuário...
                mapa = new google.maps.Map(document.getElementById('mapa'), {
                    center: userLocation,
                    zoom: 14, // Ajuste o nível de zoom conforme necessário
                
                    // Configurações do estilo do mapa para desativar os marcadores padrão
                    styles: [
                        {
                            featureType: 'poi',
                            elementType: 'labels.icon',
                            stylers: [{ visibility: 'off' }]
                        }
                    ]
                });

                // Adiciona um marcador na localização do usuário...
                var marker = new google.maps.Marker({
                    position: userLocation,
                    map: mapa,
                    title: 'Sua Localização'
                });

                // Inicializa a função de autocomplete...
                initAutocomplete();
            }, function (error) {
                console.log('Erro ao obter a localização do usuário:', error);
                initAutocomplete(); // Inicializa a função de autocomplete mesmo em caso de erro
            }, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 30000
            });
        } else {
            console.log('Seu navegador não suporta geolocalização.');
            initAutocomplete(); // Inicializa a função de autocomplete mesmo se a geolocalização não for suportada
        }
    } else {
        setTimeout(initMap, 100);
    }
}

function initAutocomplete() {
    if (google.maps.places) {
        var input = document.getElementById('id_endereco');
        autocomplete = new google.maps.places.Autocomplete(input);
        // Configurações adicionais do Autocomplete aqui...
        autocomplete.addListener('place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.geometry) {
                adicionarMarcador(place.geometry.location, place.formatted_address);
                limparInputEndereco();

            }
        });
    }
}

function adicionarMarcador(localizacao, endereco) {
    if (mapa) {
        var numeroMarcador = marcadores.length + 1; // Número sequencial do marcador
        var marker = new google.maps.Marker({
            position: localizacao,
            map: mapa,
            title: endereco,
            animation: google.maps.Animation.DROP,
            label: numeroMarcador.toString(), // Adiciona a numeração ao marcador
        });

        marker.setAnimation(google.maps.Animation.DROP);

        // Ou adicione uma janela de informações (info window)
        var infoWindow = new google.maps.InfoWindow({
            content: 'Marcador #' + numeroMarcador + '<br>Endereço: ' + endereco
        });

        marker.addListener('click', function () {
            infoWindow.open(mapa, marker);
        });

        // Pode adicionar mais personalizações ao marcador, se necessário
        // Exemplo: marker.setIcon('caminho/do/ícone.png');
        // ...

        // Centraliza o mapa na nova localização
        mapa.panTo(localizacao);

        // Adiciona o marcador ao array
        marcadores.push(marker);

        // Adiciona entrada à tabela
        adicionarEntradaTabela(numeroMarcador, endereco);

        // Limpa a lista de sugestões
        document.getElementById('sugestoes-lista').innerHTML = '';
    }
}

function limparInputEndereco() {
    document.getElementById('id_endereco').value = '';
    document.getElementById('sugestoes-lista').innerHTML = '';
}

function adicionarEntradaTabela(numero, endereco) {
    var tabela = document.getElementById('tabela-enderecos');
    var novaLinha = tabela.insertRow(-1);
    var celulaNumero = novaLinha.insertCell(0);
    var celulaEndereco = novaLinha.insertCell(1);

    celulaNumero.innerHTML = numero;
    celulaEndereco.innerHTML = endereco;
}


async function buscarEndereco() {
    try {
        await carregarAPIAutocompletar();
        var enderecoInput = document.getElementById('id_endereco').value;
        var predictions = await obterSugestoesEndereco(enderecoInput);
        
        if (predictions.length > 0) {
            exibirListaSugestoes(predictions);
        } else {
            buscarEnderecoDireto();
        }
    } catch (error) {
        console.error('Erro ao buscar endereço:', error);
    }
}

async function carregarAPIAutocompletar() {
    if (!autocomplete) {
        await loadScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyAl4N-KtLVFhvzJ6MuDua1CbN0LJSEBH1U&libraries=places');
        initAutocomplete();
    }
}

function loadScript(src) {
    return new Promise((resolve, reject) => {
        var script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

async function obterSugestoesEndereco(input) {
    return new Promise((resolve, reject) => {
        var service = new google.maps.places.AutocompleteService();
        service.getPlacePredictions(
            {
                input: input,
                componentRestrictions: { country: 'br' },
            },
            (predictions, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && predictions) {
                    resolve(predictions);
                } else {
                    reject('Erro ao obter sugestões de endereço.');
                }
            }
        );
    });
}

// Restante do seu código...
