from freezegun import freeze_time
from rest_framework.test import APITestCase
from rest_framework import status
from api.models.category import Category
from api.models.company import Company

class CategoryViewTests(APITestCase):
    def setUp(self):
        # 日時を固定する
        self.time_freeze = freeze_time("2025-06-14T00:00:00Z")
        self.time_freeze.start()

        # 念のため migration のデータを削除
        Category.objects.all().delete()
        Company.objects.all().delete()

        # テスト用のCompany/Category(parent_category用)インスタンスを作成
        self.company = Company.objects.create(name="Test Company")
        self.parent_category = Category.objects.create(name="Parent Category", company=self.company)


    def tearDown(self):
        self.time_freeze.stop()


    def test_list(self):
        url = "/api/categories/"
        # Categoryが10+1(parent_category)件取得できることを確認
        categories = [
            Category.objects.create(name=f"Category {i}", company=self.company, parent_category=self.parent_category)
            for i in range(10)
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            # parent_categoryのデータ
            {
                "id": str(self.parent_category.id),
                "company": self.company.id,
                "name": "Parent Category",
                "parent_category": None,
                "created_at": "2025-06-14T00:00:00Z",
                "updated_at": "2025-06-14T00:00:00Z"
            },
            *[
                {
                    "id": str(cat.id),
                    "company": self.company.id,
                    "name": f"Category {i}",
                    "parent_category": self.parent_category.id,
                    "created_at": "2025-06-14T00:00:00Z",
                    "updated_at": "2025-06-14T00:00:00Z",
                }
                for i, cat in enumerate(categories)
            ],
        ]

        self.assertEqual(response.data, expected_data)


    def test_retrieve(self):
        category = Category.objects.create(
            name="Retrieve Category", company=self.company, parent_category=self.parent_category
        )
        url = f"/api/categories/{category.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": str(category.id),
            "company": self.company.id,
            "name": "Retrieve Category",
                "parent_category": self.parent_category.id,
            "created_at": "2025-06-14T00:00:00Z",
            "updated_at": "2025-06-14T00:00:00Z",
        }
        self.assertEqual(response.data, expected_data)


    def test_create(self):
        url = "/api/categories/"
        data = {
            "name": "Created Category",
            "company": str(self.company.id),
            "parent_category": str(self.parent_category.id),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        created_category = Category.objects.exclude(id=self.parent_category.id).first()
        expected_data = {
            "id": str(created_category.id),
            "company": self.company.id,
            "name": "Created Category",
            "parent_category": self.parent_category.id,
            "created_at": "2025-06-14T00:00:00Z",
            "updated_at": "2025-06-14T00:00:00Z",
        }
        self.assertEqual(response.data, expected_data)


    def test_update(self):
        category = Category.objects.create(name="Old Name", company=self.company, parent_category=self.parent_category)
        url = f"/api/categories/{category.id}/"
        data = {"name": "New Name"}
        # 日時更新
        self.time_freeze = freeze_time("2025-06-14T00:00:01Z")
        self.time_freeze.start()
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "id": str(category.id),
            "company": self.company.id,
            "name": "New Name",
            "parent_category": self.parent_category.id,
            "created_at": "2025-06-14T00:00:00Z",
            "updated_at": "2025-06-14T00:00:01Z",
        }
        self.assertEqual(response.data, expected_data)


    def test_destroy(self):
        category = Category.objects.create(name="Delete Category", company=self.company, parent_category=self.parent_category)
        url = f"/api/categories/{category.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())
