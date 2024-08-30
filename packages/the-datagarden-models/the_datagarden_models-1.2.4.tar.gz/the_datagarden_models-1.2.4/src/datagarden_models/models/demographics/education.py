from pydantic import BaseModel, Field


class PercentagesByAgeGenderBaseKeys:
	MALE = "male"
	FEMALE = "female"
	TOTAL = "total"


class PercentagesByAgeGenderLegends:
	AGE_GENDER_MALE = "Percentage of males in with given education level. "
	AGE_GENDER_FEMALE = "Percentage of females with education level. "
	AGE_GENDER_TOTAL = "Percentage of females with education level. "


L1 = PercentagesByAgeGenderLegends


class PercentagesByAgeGender(BaseModel):
	male: dict = Field(default_factory=dict, description=L1.AGE_GENDER_MALE)
	female: dict = Field(default_factory=dict, description=L1.AGE_GENDER_FEMALE)
	total: dict = Field(default_factory=dict, description=L1.AGE_GENDER_TOTAL)


class Isced2011EducationLevelKeys:
	ISCED_2011_5TO8 = "isced_2011_5to8"


class Isced2011EducationLevelLegends:
	ISCED_2011_5TO8 = (
		"Level 5 up to and including level 8 of the "
		"ISCED 2011 International Standard Classification of Education."
	)


L2 = Isced2011EducationLevelLegends


class Isced2011EducationLevel(BaseModel):
	isced_2011_5to8: PercentagesByAgeGender = Field(
		default_factory=PercentagesByAgeGender, description=L2.ISCED_2011_5TO8
	)


class EducationV1Legends:
	ISCED_2011_BY_AGE_GENDER = (
		"Percentage of an age gender group with a given education level. "
		"see https://uis.unesco.org/sites/default/files/documents/international-standard-classification-of-education-isced-2011-en.pdf"
		" for detailed explenation of the education levels."
	)


L3 = EducationV1Legends


class Education(BaseModel):
	isced_2011_by_age_gender: Isced2011EducationLevel = Field(
		default_factory=Isced2011EducationLevel, description=L3.ISCED_2011_BY_AGE_GENDER
	)


class EducationV1Keys(
	PercentagesByAgeGenderBaseKeys,
	Isced2011EducationLevelKeys,
):
	ISCED_2011_BY_AGE_GENDER = "isced_2011_by_age_gender"
