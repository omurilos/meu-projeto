dados_fazenda = {}
dados_fazenda['nome_fazenda'] = input('Nome da fazenda ')
dados_fazenda['cultura'] = input('Nome da cultura ')
dados_fazenda['area'] = float(input('Area em hectar '))

pragas_capturadas = []

for i in range(5):
    capturas = int(input(f'quantas moscas foram capturadas no talhão {i+1}? '))
 
    while capturas < 0:
      print('ERRO: numero negativo. Tente novamente ')
      capturas = int(input(f'quantas moscas foram capturadas no talhão {i+1}? '))

    pragas_capturadas.append(capturas)
    
media = (sum(pragas_capturadas) / len(pragas_capturadas))
max_moscas = max(pragas_capturadas)
talhao = pragas_capturadas.index(max_moscas) + 1   


if media == 0:
    status = 'NÍVEL VERDE (Situação controlada)'
    dose_info = 'Não é necessário aplicar defensivo.'
elif media < 5:
    status = 'NÍVEL AMARELO (Atenção - aumentar vistorias)'
    dose_info = 'Monitoramento reforçado, sem aplicação no momento.'
else:
    status = 'NÍVEL VERMELHO (Ação imediata necessária)'
    dose = dados_fazenda['area'] * 1.5
    dose_info = f'Dose recomendada de defensivo: {dose:.2f} unidades'

print('\n' + '='*50)
print('RELATÓRIO DE MONITORAMENTO DE PRAGAS')
print('='*50)

print(f'Fazenda: {dados_fazenda["nome_fazenda"]}')
print(f'Cultura: {dados_fazenda["cultura"]}')
print(f'Área: {dados_fazenda["area"]:.2f} ha')


print('\nResumo:')
print(f'• Média de capturas: {media:.2f}')
print(f'• Pico máximo: {max_moscas} moscas (Talhão {talhao})')

print('\nStatus:')
print(status)
print(dose_info)

print('='*50)
    

    