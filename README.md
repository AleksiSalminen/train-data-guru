# Train Data Guru

---

## Resursseja

GraphQL:
https://www.digitraffic.fi/rautatieliikenne/#graphql
Esimerkkejä:
https://www.digitraffic.fi/rautatieliikenne/#esimerkkej%C3%A4
GraphQL-kysely omassa sovelluksessa
https://www.digitraffic.fi/rautatieliikenne/#graphql-kysely-omassa-sovelluksessa
GraphiQL, GraphQL-kyselyjen testaus selaimessa
https://rata.digitraffic.fi/api/v2/graphql/graphiql?path=/api/v2/graphql/graphql

---

## Esimerkkejä

Kaikki kulussa olevat VR:n junat ja niille viimeisin sijainti, jossa nopeus on yli 30 km/h

```javascript
{
  currentlyRunningTrains(where: {operator: {shortCode: {equals: "vr"}}}) {
    trainNumber
    departureDate
    trainLocations(where: {speed: {greaterThan: 30}}, orderBy: {timestamp: DESCENDING}, take: 1) {
      speed
      timestamp
      location
    }
  }
}
```

Kaikki junat tietyltä päivämäärältä, joiden operaattori on VR ja lähilinjaliikennetunnus ei ole Z
järjestettynä laskevasti junanumeron mukaan

```javascript
{
  trainsByDepartureDate(
    departureDate: "2020-10-05",
    where: {and: [ {operator: {shortCode: {equals: "vr"}}}, {commuterLineid: {unequals: "Z"}}]},
    orderBy: {trainNumber: DESCENDING})
  {
    trainNumber
    departureDate
    commuterLineid
    operator {
      shortCode
    }
  }
}
```

Kulussa olevat junat järjestetynä operaattorilla ja junanumerolla

```javascript
{
  currentlyRunningTrains(orderBy: [{operator:{shortCode:ASCENDING}},{trainNumber:ASCENDING}]) {
    operator {
      shortCode
    }
    trainNumber
  }
}
```
