from rest_framework import serializers

from .models import Administrador, Aluno, Funcionario, Usuario

# Serializers servem para validação de entrada e saída dos dados da API, convertendo os objetos do Django em formatos como JSON e vice-versa.
# Eles também permitem personalizar a forma como os dados são representados e validados, garantindo que a API seja consistente e fácil de usar.

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ["id", "nome", "email", "perfil", "password", "is_active"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for atributo, valor in validated_data.items():
            setattr(instance, atributo, valor)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdministradorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Administrador
        fields = ["id", "nome", "email", "perfil", "password", "is_active"]
        read_only_fields = ["id", "perfil"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        administrador = Administrador(**validated_data)
        if password:
            administrador.set_password(password)
        administrador.save()
        return administrador

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for atributo, valor in validated_data.items():
            setattr(instance, atributo, valor)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class FuncionarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Funcionario
        fields = ["id", "nome", "email", "perfil", "id_funcionario", "password", "is_active"]
        read_only_fields = ["id", "perfil"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        funcionario = Funcionario(**validated_data)
        if password:
            funcionario.set_password(password)
        funcionario.save()
        return funcionario

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for atributo, valor in validated_data.items():
            setattr(instance, atributo, valor)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AlunoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "email",
            "perfil",
            "cpf",
            "plano",
            "modalidades_inscritas",
            "password",
            "is_active",
        ]
        read_only_fields = ["id", "perfil"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        aluno = Aluno(**validated_data)
        if password:
            aluno.set_password(password)
        aluno.save()
        return aluno

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        modalidades_inscritas = validated_data.pop("modalidades_inscritas", None)

        for atributo, valor in validated_data.items():
            setattr(instance, atributo, valor)

        if password:
            instance.set_password(password)

        instance.save()

        if modalidades_inscritas is not None:
            instance.modalidades_inscritas.set(modalidades_inscritas)

        return instance
