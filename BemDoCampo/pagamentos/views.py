from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from usuarios.models import Usuarios 
import json

class CarrinhoView(View):
    template_name = 'carrinho.html'

    def get(self, request):
        produtos = []
        total = 0
        for x in range(1, 11):
            produtos.append({
                'nome': f'Produto {x}',
                'tipo': f'Tipo {x}',
                'quantidade': x,
                'preco': x,
                'unidade_medida': f'uni {x}'
            })

            total += x

        context = {
            'items': {
                'produtos': produtos,
                'total': total,
                'quantidade': len(produtos)
            }
        }

        return render(request, self.template_name, context=context)

@method_decorator(csrf_exempt, name='dispatch')
class FinalizarCompraView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validação dos campos obrigatórios
            campos_obrigatorios = ['itens', 'endereco', 'pagamento', 'cpf', 'valor_total', 'quantidade_total']
            for campo in campos_obrigatorios:
                if campo not in data or not data[campo]:
                    return JsonResponse({"error": f"O campo {campo} é obrigatório."}, status=400)
            
            itens = data.get('itens', [])
            endereco = data.get('endereco')
            pagamento = data.get('pagamento')
            cpf = data.get('cpf')
            valor_total = data.get('valor_total')
            quantidade_total = data.get('quantidade_total')

            # Criar um dicionário para a compra
            compra = {
                "itens": itens,
                "endereco": endereco,
                "pagamento": pagamento,
                "cpf": cpf,
                "valor_total": valor_total,
                "quantidade_total": quantidade_total,
                "data_compra": now(),
            }

            # Buscar o usuário na coleção 'usuarios' usando o CPF
            usuario = Usuarios.objects.filter(documento=cpf).first()  # Usando o modelo de Usuarios

            if not usuario:
                return JsonResponse({"error": "Usuário não encontrado."}, status=404)

            # Adicionar a compra dentro do documento do usuário na coleção 'usuarios'
            usuario.update(push__compras=compra)  

            return JsonResponse({"message": "Compra registrada com sucesso!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)
