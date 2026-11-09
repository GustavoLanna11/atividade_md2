import csv
from collections import Counter, defaultdict
import statistics

def main():
    # Se o arquivo estiver dentro da pasta docs:
    arquivo_csv = 'docs/Pratica_DSM6_Exames_Laboratoriais.csv'
    
    # 1. LEITURA E PREPARAÇÃO OBRIGATÓRIA
    with open(arquivo_csv, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        linhas_brutas = list(reader)
        
    r01_total_linhas = len(linhas_brutas)
    
    # Deduplicação por id_exame (mantendo a primeira ocorrência) e padronização de unidades
    vistos = set()
    dados_unicos = []
    duplicados_descartados = 0
    
    for row in linhas_brutas:
        id_ex = row['id_exame'].strip()
        if id_ex not in vistos:
            vistos.add(id_ex)
            # Padronizar nome da unidade: remover espaços e harmonizar Title Case
            row['unidade'] = row['unidade'].strip().title()
            dados_unicos.append(row)
        else:
            duplicados_descartados += 1
            
    r02_duplicados = duplicados_descartados
    r02_unicos = len(dados_unicos)
    
    # Tratamento de ausentes em tempo_processamento_h e valor_rs (conversão condicional)
    aus_tempo = sum(1 for r in dados_unicos if not r['tempo_processamento_h'].strip())
    aus_valor = sum(1 for r in dados_unicos if not r['valor_rs'].strip())
    aus_turno = sum(1 for r in dados_unicos if not r['turno'].strip())

    print("=" * 60)
    print(" RELATÓRIOS OPERACIONAIS - LABORATÓRIO VIDA & DADOS")
    print("=" * 60)
    

    # BLOCO A – Relatórios de qualidade e produção
    print(f"\n[R01] Quantidade total de linhas originalmente importadas: {r01_total_linhas}")
    print(f"[R02] Registros duplicados descartados: {r02_duplicados} | Exames únicos finais: {r02_unicos}")
    print(f"[R03] Valores ausentes -> Tempo de processamento: {aus_tempo} | Valor financeiro (R$): {aus_valor} | Turno: {aus_turno}")
    
    # R04. Quantidade de exames por unidade, em ordem alfabética
    unidades_count = Counter(r['unidade'] for r in dados_unicos)
    print("\n[R04] Quantidade de exames por unidade (ordem alfabética):")
    for unidade, qtd in sorted(unidades_count.items()):
        print(f"  - {unidade}: {qtd}")
        
    # R05. Quantidade de exames por tipo_exame, em ordem alfabética
    tipos_count = Counter(r['tipo_exame'].strip() for r in dados_unicos)
    print("\n[R05] Quantidade de exames por tipo (ordem alfabética):")
    for tipo, qtd in sorted(tipos_count.items()):
        print(f"  - {tipo}: {qtd}")
        
    # R06. Quantidade de exames por prioridade, distinguindo Rotina e Urgente
    prio_count = Counter(r['prioridade'].strip() for r in dados_unicos)
    print("\n[R06] Quantidade de exames por prioridade:")
    print(f"  - Rotina: {prio_count.get('Rotina', 0)}")
    print(f"  - Urgente: {prio_count.get('Urgente', 0)}")
    
    # R07. Quantidade de exames em cada turno, incluindo “Nao informado”
    turnos_list = []
    for r in dados_unicos:
        t = r['turno'].strip()
        if not t:
            turnos_list.append('Nao informado')
        else:
            turnos_list.append(t.title())
    turno_count = Counter(turnos_list)
    print("\n[R07] Quantidade de exames por turno:")
    for turno, qtd in sorted(turno_count.items()):
        print(f"  - {turno}: {qtd}")
        
    # R08. Percentual de exames que exigiram recoleta em cada unidade
    recoleta_unidade = defaultdict(lambda: {'total': 0, 'recoleta': 0})
    for r in dados_unicos:
        u = r['unidade']
        recoleta_unidade[u]['total'] += 1
        if r['recoleta'].strip().lower() in ['sim', 's']:
            recoleta_unidade[u]['recoleta'] += 1
            
    print("\n[R08] Percentual de exames que exigiram recoleta por unidade:")
    for unidade, d in sorted(recoleta_unidade.items()):
        perc = (d['recoleta'] / d['total']) * 100 if d['total'] > 0 else 0
        print(f"  - {unidade}: {d['recoleta']} de {d['total']} ({perc:.2f}%)")

    # BLOCO B – Relatórios analíticos e classificação
    print("\n" + "-" * 60)
    
    # R09. Valor financeiro total e valor médio por tipo de exame
    tipo_valores = defaultdict(list)
    for r in dados_unicos:
        t = r['tipo_exame'].strip()
        val_str = r['valor_rs'].strip()
        if val_str:
            try:
                tipo_valores[t].append(float(val_str))
            except ValueError:
                pass
                
    print("\n[R09] Valor financeiro total e médio por tipo de exame:")
    for tipo, valores in sorted(tipo_valores.items()):
        total_val = sum(valores)
        media_val = total_val / len(valores) if valores else 0
        print(f"  - {tipo}: Total = R$ {total_val:.2f} | Média = R$ {media_val:.2f} (N={len(valores)})")
        
    # R10. Tempo médio e mediana de processamento por prioridade
    prio_tempos = defaultdict(list)
    for r in dados_unicos:
        p = r['prioridade'].strip()
        tempo_str = r['tempo_processamento_h'].strip()
        if tempo_str:
            try:
                prio_tempos[p].append(float(tempo_str))
            except ValueError:
                pass
                
    print("\n[R10] Tempo médio e mediana de processamento por prioridade:")
    for prio, tempos in sorted(prio_tempos.items()):
        media_t = statistics.mean(tempos) if tempos else 0
        mediana_t = statistics.median(tempos) if tempos else 0
        print(f"  - {prio}: Média = {media_t:.2f}h | Mediana = {mediana_t:.2f}h (N={len(tempos)})")
        
    # R11. Percentual de exames com atraso real por unidade
    atraso_unidade = defaultdict(lambda: {'total': 0, 'atraso': 0})
    for r in dados_unicos:
        u = r['unidade']
        atraso_unidade[u]['total'] += 1
        if r['atraso'].strip().lower() in ['sim', 's']:
            atraso_unidade[u]['atraso'] += 1
            
    print("\n[R11] Percentual de exames com atraso real por unidade:")
    for unidade, d in sorted(atraso_unidade.items()):
        perc_atraso = (d['atraso'] / d['total']) * 100 if d['total'] > 0 else 0
        print(f"  - {unidade}: {d['atraso']} de {d['total']} ({perc_atraso:.2f}%)")
        
    # R12. Os três tipos de exame mais frequentes, ordenados por quantidade
    top3_tipos = tipos_count.most_common(3)
    print("\n[R12] Três tipos de exame mais frequentes:")
    for rank, (tipo, qtd) in enumerate(top3_tipos, 1):
        print(f"  {rank}º {tipo}: {qtd} exames")
        
    # R13. Alerta operacional (Matriz de Confusão: TP, FP, FN, TN)
    tp = fp = fn = tn = 0
    ignorados_tempo = 0
    
    for r in dados_unicos:
        tempo_str = r['tempo_processamento_h'].strip()
        if not tempo_str:
            ignorados_tempo += 1
            continue
        try:
            tempo = float(tempo_str)
        except ValueError:
            ignorados_tempo += 1
            continue
            
        prio = r['prioridade'].strip().lower()
        atraso_real = r['atraso'].strip().lower() in ['sim', 's']
        
        # Regra de Alerta: Rotina >= 20h ou Urgente >= 3h
        pred_risco = False
        if prio == 'rotina' and tempo >= 20:
            pred_risco = True
        elif prio == 'urgente' and tempo >= 3:
            pred_risco = True
            
        if pred_risco and atraso_real:
            tp += 1
        elif pred_risco and not atraso_real:
            fp += 1
        elif not pred_risco and atraso_real:
            fn += 1
        elif not pred_risco and not atraso_real:
            tn += 1
            
    print(f"\n[R13] Matriz de Confusão (Alerta Operacional):")
    print(f"  - Verdadeiros Positivos (TP): {tp}")
    print(f"  - Falsos Positivos (FP): {fp}")
    print(f"  - Falsos Negativos (FN): {fn}")
    print(f"  - Verdadeiros Negativos (TN): {tn}")
    print(f"  (Registros sem tempo de processamento excluídos da avaliação: {ignorados_tempo})")
    
    # R14. Precisão e Revocação (0 a 1 com 4 casas decimais)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print(f"\n[R14] Métricas de Classificação do Alerta:")
    print(f"  - Precision (Precisão): {precision:.4f}")
    print(f"  - Recall (Revocação): {recall:.4f}")
    
    # R15. Decisão gerencial e limitação da regra
    r15_texto = (
        "\n[R15] Análise Gerencial e Limitações:\n"
        "  Decisão gerencial possível: A coordenação operacional pode utilizar o "
        "sistema de alertas automáticos em tempo real para realocar equipes de "
        "apoio para unidades ou turnos que apresentem risco iminente de extrapolação "
        "de prazos, mitigando gargalos antes que o atraso se concretize.\n"
        "  Limitação da regra de classificação: A regra baseia-se em limiares estáticos "
        "de tempo (ex: 20h para rotina), desconsiderando fatores contextuais complexos "
        "como o volume simultâneo de amostras, picos sazonais ou manutenções imprevistas "
        "de equipamentos, o que pode gerar alarmes falsos (FP) ou ignorar atrasos "
        "atípicos em cenários de alta eficiência."
    )
    print(r15_texto)
    print("=" * 60)

if __name__ == '__main__':
    main()