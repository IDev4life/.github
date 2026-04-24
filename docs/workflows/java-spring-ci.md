# `java-spring-ci.yml` — CI cho Java / Spring

Chạy test Maven hoặc Gradle kèm **JUnit annotation trên PR diff**, xuất artifact test report, và (tuỳ chọn) upload JaCoCo coverage lên Codecov.

## Trigger

`workflow_call`

## Inputs

| Input               | Bắt buộc | Mặc định        | Mô tả                                                |
| ------------------- | -------- | --------------- | ---------------------------------------------------- |
| `java_version`      | ❌       | `21`            | Java major version (hỗ trợ 21 LTS, 17 LTS, ...)      |
| `java_distribution` | ❌       | `temurin`       | `temurin` / `corretto` / `zulu` / ...                |
| `build_tool`        | ❌       | `maven`         | `maven` hoặc `gradle`                                |
| `working_directory` | ❌       | `.`             | Thư mục làm việc (dùng cho monorepo)                 |
| `maven_args`        | ❌       | `-B -ntp`       | Args bổ sung cho `./mvnw verify`                     |
| `gradle_args`       | ❌       | `""`            | Args bổ sung cho `./gradlew check`                   |
| `upload_coverage`   | ❌       | `true`          | Upload JaCoCo XML lên Codecov nếu có `CODECOV_TOKEN` |
| `runs_on`           | ❌       | `ubuntu-latest` | Runner label                                         |

## Secrets

| Secret               | Bắt buộc | Ghi chú                                   |
| -------------------- | -------- | ----------------------------------------- |
| `CODECOV_TOKEN`      | ❌       | Không có thì bước upload coverage tự skip |
| `TELEGRAM_BOT_TOKEN` | ❌       | Forward cho notify (nếu chain)            |
| `TELEGRAM_CHAT_ID`   | ❌       | Forward cho notify (nếu chain)            |

## Permissions (khai báo ở caller)

```yaml
permissions:
  contents: read
  checks: write # JUnit annotation
  pull-requests: write # coverage PR comment
```

## Cách dùng

### Maven

```yaml
jobs:
  test:
    permissions:
      contents: read
      checks: write
      pull-requests: write
    uses: IDev4life/.github/.github/workflows/java-spring-ci.yml@main
    with:
      java_version: "21"
      build_tool: maven
    secrets: inherit
```

### Gradle + monorepo

```yaml
jobs:
  test:
    uses: IDev4life/.github/.github/workflows/java-spring-ci.yml@main
    with:
      java_version: "21"
      build_tool: gradle
      working_directory: services/api
      gradle_args: "--parallel"
    secrets: inherit
```

### Chain với docker-build

```yaml
jobs:
  test:
    uses: IDev4life/.github/.github/workflows/java-spring-ci.yml@main
    secrets: inherit
  image:
    needs: test
    uses: IDev4life/.github/.github/workflows/docker-build.yml@main
    with:
      image_name: IDev4life/my-spring-app
    secrets: inherit
```

## Đầu ra

- **JUnit annotation:** bình luận trực tiếp trên dòng test fail ở PR diff (qua `mikepenz/action-junit-report@v6.4.0`), `fail_on_failure: true`.
- **Coverage:** JaCoCo XML (`target/site/jacoco/jacoco.xml` hoặc `build/reports/jacoco/test/jacocoTestReport.xml`) lên Codecov với flag `java`.
- **Artifact `java-test-reports`:** raw reports Surefire / Failsafe / Gradle test-results, giữ 7 ngày để debug.

## Path mà workflow quét

```
<working_directory>/**/target/surefire-reports/TEST-*.xml
<working_directory>/**/target/failsafe-reports/TEST-*.xml
<working_directory>/**/build/test-results/**/TEST-*.xml
```

## Lưu ý

- Maven chạy `./mvnw --fail-fast <maven_args> verify` — yêu cầu repo có Maven Wrapper (`mvnw`).
- Gradle chạy `./gradlew --no-daemon --continue check <gradle_args>` — yêu cầu Gradle Wrapper (`gradlew`).
- Cache được `setup-java@v5.2.0` tự xử lý theo `build_tool`.
