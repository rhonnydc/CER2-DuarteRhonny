from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, LugarPatrimonial


class CatalogoYPermisosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre='Murales')
        cls.otra_categoria = Categoria.objects.create(nombre='Monumentos')
        cls.lugar = LugarPatrimonial.objects.create(
            nombre='Mural de prueba', descripcion='Descripción',
            ubicacion='Valparaíso', categoria=cls.categoria,
        )
        LugarPatrimonial.objects.create(
            nombre='Monumento de prueba', descripcion='Descripción',
            ubicacion='Santiago', categoria=cls.otra_categoria,
        )
        cls.lector = User.objects.create_user('lector', password='clave-segura-123')
        cls.editor = User.objects.create_user('editor', password='clave-segura-123')
        cls.editor.user_permissions.add(
            Permission.objects.get(codename='add_lugarpatrimonial'),
            Permission.objects.get(codename='change_lugarpatrimonial'),
        )

    def test_catalogo_publico_y_filtro(self):
        respuesta = self.client.get(reverse('catalogo'))
        self.assertContains(respuesta, 'Mural de prueba')
        self.assertContains(respuesta, 'Monumento de prueba')
        respuesta = self.client.get(reverse('catalogo_categoria', args=[self.categoria.pk]))
        self.assertContains(respuesta, 'Mural de prueba')
        self.assertNotContains(respuesta, 'Monumento de prueba')
        self.assertContains(self.client.get(reverse('detalle', args=[self.lugar.pk])), 'Valparaíso')

    def test_gestion_exige_sesion(self):
        respuesta = self.client.get(reverse('gestion'))
        self.assertRedirects(respuesta, '/ingresar/?next=/gestion/')
        self.assertEqual(self.client.get(reverse('agregar_lugar')).status_code, 302)
        self.assertEqual(self.client.get(reverse('editar_lugar', args=[self.lugar.pk])).status_code, 302)
        self.client.force_login(self.lector)
        self.assertEqual(self.client.get(reverse('gestion')).status_code, 200)

    def test_inicio_y_cierre_de_sesion(self):
        respuesta = self.client.post(reverse('login'), {
            'username': 'lector', 'password': 'clave-segura-123',
        })
        self.assertRedirects(respuesta, reverse('gestion'))
        self.assertEqual(self.client.get(reverse('gestion')).status_code, 200)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('home'))
        self.assertEqual(self.client.get(reverse('gestion')).status_code, 302)

    def test_lector_no_puede_agregar_ni_editar_por_url(self):
        self.client.force_login(self.lector)
        datos = {
            'nombre': 'Cambio indebido', 'categoria': self.categoria.pk,
            'descripcion': 'Prueba', 'ubicacion': 'Prueba',
            'anio_construccion': '', 'imagen': '',
        }
        self.assertEqual(self.client.get(reverse('agregar_lugar')).status_code, 403)
        self.assertEqual(self.client.post(reverse('agregar_lugar'), datos).status_code, 403)
        self.assertEqual(self.client.get(reverse('editar_lugar', args=[self.lugar.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse('editar_lugar', args=[self.lugar.pk]), datos).status_code, 403)
        self.assertFalse(LugarPatrimonial.objects.filter(nombre='Cambio indebido').exists())

    def test_editor_puede_agregar_y_editar(self):
        self.client.force_login(self.editor)
        datos = {
            'nombre': 'Lugar nuevo', 'categoria': self.categoria.pk,
            'descripcion': 'Prueba', 'ubicacion': 'Valparaíso',
            'anio_construccion': '1900', 'imagen': '',
        }
        respuesta = self.client.post(reverse('agregar_lugar'), datos)
        self.assertEqual(respuesta.status_code, 302)
        lugar = LugarPatrimonial.objects.get(nombre='Lugar nuevo')
        datos['nombre'] = 'Lugar corregido'
        respuesta = self.client.post(reverse('editar_lugar', args=[lugar.pk]), datos)
        self.assertEqual(respuesta.status_code, 302)
        lugar.refresh_from_db()
        self.assertEqual(lugar.nombre, 'Lugar corregido')
